from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context
import json
import random
import time



@AgentServer.custom_action("切换队伍")
class ChangeTeam(CustomAction):

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:
        team_roi = [
            [0,0,0,0],
            [56,117,22,15],
            [127,115,26,23],
            [204,113,16,25],
            [270,113,35,26],
            [349,117,22,22],
            [416,112,23,32],
            [494,113,30,28],
            [565,113,30,29]
        ]
        json_data = json.loads(argv.custom_action_param)
        team_index = int(json_data.get('队伍序号'))
        if team_index != 0:
            context.run_task("custom", {
            "custom": {
                "target": team_roi[team_index],
                "action": "Click",
            }
        })
        return True


@AgentServer.custom_action("调整巨兽等级")
class ChangeMonsterLevel(CustomAction):

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:
        return True


@AgentServer.custom_action("开始出征")
class BeginCombat(CustomAction):
    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:
        json_data = json.loads(argv.custom_action_param)
        print(json_data)        
        # TODO:智能化
        #if combat_times == 0:
        #    return True
        
        # 获取返回时间
        img = context.tasker.controller.post_screencap().wait().get()
        detail = context.run_recognition("识别时间", img)
        # print("time:",detail)
        hours, minutes, seconds = map(int, detail.best_result.text.split(':'))
        return_time = hours * 3600 + minutes * 60 + seconds
        
        # 开始出征
        context.run_task("点击出征")
        time.sleep(0.5)
        img = context.tasker.controller.post_screencap().wait().get()    
        detail = context.run_recognition("集结中", img)
        # print(f'detail: {detail}')
        if detail is not None and detail.box:
                # print(f'detail box: {detail.box}')
                # print(f'x,y:{6 + detail.box.x + 195},{detail.box.y}')
                context.tasker.controller.post_click(
                    6 + detail.box.x + 195, detail.box.y
                    
                ).wait()
                
                detail = None
                while detail is None:
                    time.sleep(1)
                    img = context.tasker.controller.post_screencap().wait().get()
                    detail = context.run_recognition("行军中",img)
                context.run_task("后退")
                time.sleep(return_time*2 + 2)
                context.run_task("集结冰原巨兽起点")
                return True
        return True
    
@AgentServer.custom_action("灯塔开始出征")
class LightBeginCombat(CustomAction):
    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:
        json_data = json.loads(argv.custom_action_param)
        print(json_data)        
        img = context.tasker.controller.post_screencap().wait().get()
        detail = context.run_recognition("识别时间", img)
        # print("time:",detail)
        hours, minutes, seconds = map(int, detail.best_result.text.split(':'))
        return_time = hours * 3600 + minutes * 60 + seconds
        
        # 开始出征
        context.run_task("点击出征")
        time.sleep(return_time*2 + 2)
        context.run_task("灯塔入口")        
        return True