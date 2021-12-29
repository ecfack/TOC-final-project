from transitions.extensions import GraphMachine
import datetime
from utils import send_text_message,send_image_url
import crawler


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.user_data=dict()
    def is_going_to_state1(self, event):
        text = event.message.text

        if "增" == text[0]:
          return True  
        return False
        # return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        if "查" == text[0]:
          return True  
        return False
        # return text.lower() == "go to state2"

    def is_going_to_state3(self, event):
        text = event.message.text
        if "刪" == text[0]:
          return True  
        return False

    def is_going_to_state4(self, event):
        text = event.message.text
        if "改" == text[0]:
          return True  
        return False
    
    def is_going_to_state5(self, event):
        text = event.message.text
        if "日出" == text:
          return True  
        return False
    
    def is_going_to_state6(self, event):
        text = event.message.text
        if "解說" == text[0:2]:
          return True  
        return False
    
    def is_going_to_state7(self, event):
        text = event.message.text
        if "日落" == text:
          return True  
        return False
    
    def is_going_to_state8(self, event):
        text = event.message.text
        if "FSM" == text:
          return True  
        return False
    
    def is_going_to_state9(self, event):
        text = event.message.text
        if "還說不能傳空訊息" == text:
          return True  
        return False

    def on_enter_state1(self, event):   #增 new_task1 new_task2...
        print("I'm entering state1")

        #從event抓資料
        text = event.message.text
        uid=event.source.user_id
        reply_token = event.reply_token

        #初始化新user
        if uid not in self.user_data:
            self.user_data[uid]=dict()
        
        #字串處理
        db_tasks=self.user_data[uid]
        text=text[1:]
        text=str(text).strip(" ")
        tasks=text.split(" ")

        #塞進DB
        for task in tasks:
            db_tasks[task]=len(db_tasks)+1
        
        #打印tasks
        output_tasks=sorted(self.user_data[uid].items(), key=lambda x:x[1])
        output_str="新增成功!!\nTask:"
        for i in range(0,len(output_tasks)):
            output_str+=("\n"+str(i+1)+". "+str(output_tasks[i][0]))
        print(self.user_data[uid])
        send_text_message(reply_token, output_str)
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):   #查
        print("I'm entering state2")

        #從event抓資料
        reply_token = event.reply_token
        uid=event.source.user_id

        #初始化新user
        if uid not in self.user_data:
            self.user_data[uid]=dict()
        #打印tasks
        output_tasks=sorted(self.user_data[uid].items(), key=lambda x:x[1])
        output_str="查詢成功!!\nTask:"
        for i in range(0,len(output_tasks)):
            output_str+=("\n"+str(i+1)+". "+str(output_tasks[i][0]))
        print(self.user_data[uid])
        send_text_message(reply_token, output_str)
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
    
    def on_enter_state3(self, event):   #刪 old_tasks1 old_tasks2...
        print("I'm entering state3")

        #從event抓資料
        text = event.message.text
        reply_token = event.reply_token
        uid=event.source.user_id

        #初始化新user
        if uid not in self.user_data:
            self.user_data[uid]=dict()
        
        #字串處理
        text=text[1:]
        text=str(text).strip(" ")
        tasks=text.split(" ")

        if(len(text)):
            #刪除tasks
            if(text[0]=="*"):
                self.user_data[uid]=dict()
            else:
                delelte_list=[]
                for task in tasks:
                    for key,value in self.user_data[uid].items():
                        if value == int(task):
                            delelte_list.append(key)
                for key in delelte_list:
                    del self.user_data[uid][key]
        
        #重新排序
        i=1
        for task,number in self.user_data[uid].items():
            self.user_data[uid][task]=i
            i+=1

        #打印tasks
        output_tasks=sorted(self.user_data[uid].items(), key=lambda x:x[1])
        output_str="刪除成功!!\nTask:"
        for i in range(0,len(output_tasks)):
            output_str+=("\n"+str(i+1)+". "+str(output_tasks[i][0]))
        print(self.user_data[uid])
        send_text_message(reply_token, output_str)
        self.go_back()

    def on_exit_state3(self):
        print("Leaving state3")

    def on_enter_state4(self, event):   #改 old_task new_task
        print("I'm entering state4")

        #從event抓資料
        text = event.message.text
        reply_token = event.reply_token
        uid=event.source.user_id

        #初始化新user
        if uid not in self.user_data:
            self.user_data[uid]=dict()
        
        #字串處理
        text=text[1:]
        text=str(text).strip(" ")
        tasks=text.split(" ")

        #修改對應task內容
        if(len(tasks)>=2):
            old_task=tasks[0]
            new_task=tasks[1]
            if old_task in self.user_data[uid]:
                number=self.user_data[uid][old_task]
                del self.user_data[uid][old_task]
                self.user_data[uid][new_task]=number

        #打印tasks
        output_tasks=sorted(self.user_data[uid].items(), key=lambda x:x[1])
        output_str="修改成功!!\nTask:"
        for i in range(0,len(output_tasks)):
            output_str+=("\n"+str(i+1)+". "+str(output_tasks[i][0]))
        print(self.user_data[uid])
        send_text_message(reply_token, output_str)
        self.go_back()

    def on_exit_state4(self):
        print("Leaving state4")
    
    def on_enter_state5(self, event):   #日出
        print("I'm entering state5")

        #從event抓資料
        reply_token = event.reply_token
        uid=event.source.user_id

        #爬日出時間
        sunrise_times=crawler.fetch_sun_time()
        
        output_str="查詢成功!!\n日出時間:"
        output_str+=("\n今天: "+str(sunrise_times[0]))
        output_str+=("\n明天: "+str(sunrise_times[2]))
        send_text_message(reply_token, output_str)
        self.go_back()

    def on_exit_state5(self):
        print("Leaving state5")
    
    def on_enter_state6(self, event):   #解說指令
        print("I'm entering state6")
        self.go_back()

    def on_exit_state6(self):
        print("Leaving state6")

    def on_enter_state7(self, event):   #日落
        print("I'm entering state5")

        #從event抓資料
        reply_token = event.reply_token
        uid=event.source.user_id

        #爬日出時間
        sundown_times=crawler.fetch_sun_time()
        
        output_str="查詢成功!!\n日落時間:"
        output_str+=("\n今天: "+str(sundown_times[1]))
        output_str+=("\n明天: "+str(sundown_times[3]))
        send_text_message(reply_token, output_str)
        self.go_back()

    def on_exit_state7(self):
        print("Leaving state7")
    
    def on_enter_state8(self, event):   #FSM
        print("I'm entering state8")
        reply_token = event.reply_token
        send_image_url(reply_token, "https://6294-2001-b400-e73c-9a73-a550-6d9a-effb-247b.ngrok.io/show-fsm")
        self.go_back()

    def on_exit_state8(self):
        print("Leaving state8")
    
    def on_enter_state9(self, event):   #可憐啊
        print("I'm entering state9")
        reply_token = event.reply_token
        send_image_url(reply_token,"https://memeprod.sgp1.digitaloceanspaces.com/meme/a9a16134b16c3a8d71fbd3ea723f9efe.png")
        self.go_back()

    def on_exit_state9(self):
        print("Leaving state9")