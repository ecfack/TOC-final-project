from transitions.extensions import GraphMachine


import datetime


from utils import send_text_message, send_image_url


import crawler


import os


import redis


class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):

        self.machine = GraphMachine(model=self, **machine_configs)
        DB_IP = os.environ.get("DB_IP", "0.0.0.1")
        DB_PORT = os.environ.get("DB_PORT", "3000")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "abcd")
        self.conn_pool = redis.ConnectionPool(
            host=DB_IP, port=DB_PORT,password=DB_PASSWORD, decode_responses=True)

        self.r = redis.Redis(connection_pool=self.conn_pool)

    def is_going_to_create_state(self, event):

        text = event.message.text

        if "增" == text[0]:

            return True

        return False

        # return text.lower() == "go to create_state"

    def is_going_to_read_state(self, event):

        text = event.message.text

        if "查" == text[0]:

            return True

        return False

        # return text.lower() == "go to read_state"

    def is_going_to_delete_state(self, event):

        text = event.message.text

        if "刪" == text[0]:

            return True

        return False

    def is_going_to_update_state(self, event):

        text = event.message.text

        if "改" == text[0]:

            return True

        return False

    def is_going_to_sunrise_state(self, event):

        text = event.message.text

        if "日出" == text:

            return True

        return False

    def is_going_to_explain_state(self, event):

        text = event.message.text

        if "解說" == text[0:2]:

            return True

        return False

    def is_going_to_sunset_state(self, event):

        text = event.message.text

        if "日落" == text:

            return True

        return False

    def is_going_to_FSM_state(self, event):

        text = event.message.text

        if "FSM" == text:

            return True

        return False

    def is_going_to_murmur_state(self, event):

        text = event.message.text

        if "也不能傳空訊息" == text:

            return True

        return False

    def on_enter_create_state(self, event):  # 增 new_task1 new_task2...

        print("I'm entering create_state")

        # 從event抓資料
        text = event.message.text
        uid = event.source.user_id
        reply_token = event.reply_token
        
        try:
            # 字串處理
            text = text[1:]
            text = str(text).strip(" ")
            tasks = text.split(" ")

            # 塞進DB
            temp_dict=dict()
            for task in tasks:
                timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                temp_dict[task]=timestamp
            self.r.hmset(uid,temp_dict)
        except:
            pass
        finally:
            # 打印tasks
            output_tasks = self.r.hgetall(uid)
            output_tasks=sorted(output_tasks.items(), key=lambda x:x[1])
            output_str = "新增成功!!\nTask:"

            for i in range(0, len(output_tasks)):
                output_str += ("\n"+str(i+1)+". "+str(output_tasks[i][0]))
            print(output_tasks)

            # 七天後到期
            self.r.expire(uid, 60*60*24*7)

            # 送出res
            send_text_message(reply_token, output_str)
            self.go_back()

    def on_exit_create_state(self):
        print("Leaving create_state")

    def on_enter_read_state(self, event):  # 查
        print("I'm entering read_state")

        # 從event抓資料
        reply_token = event.reply_token
        uid = event.source.user_id

        # 打印tasks
        output_tasks = self.r.hgetall(uid)
        output_tasks = sorted(output_tasks.items(), key=lambda x: x[1])

        output_str = "查詢成功!!\nTask:"

        for i in range(0, len(output_tasks)):
            output_str += ("\n"+str(i+1)+". "+str(output_tasks[i][0]))
        print(output_tasks)

        # 七天後到期
        self.r.expire(uid, 60*60*24*7)

        # 送出res
        send_text_message(reply_token, output_str)
        self.go_back()

    def on_exit_read_state(self):

        print("Leaving read_state")

    def on_enter_delete_state(self, event):  # 刪 old_tasks1 old_tasks2...

        print("I'm entering delete_state")

        # 從event抓資料
        text = event.message.text
        reply_token = event.reply_token
        uid = event.source.user_id

        try:
            # 字串處理
            text = text[1:]
            text = str(text).strip(" ")
            tasks = text.split(" ")

            if(len(text)):
                # 刪除tasks
                if(text[0] == "*"):
                    self.r.delete(uid)

                else:
                    output_tasks = self.r.hgetall(uid)
                    output_tasks = sorted(output_tasks.items(), key=lambda x: x[1])

                    pipe=self.r.pipeline()
                    for task_num in tasks:
                        for task_pair in output_tasks:
                            if task_pair[1] == int(task_num):
                                self.r.hdel(uid,task_pair[0])
                                break
                    pipe.execute()
        except:
            pass
        finally:
            # 打印tasks
            output_tasks = self.r.hgetall(uid)
            output_tasks = sorted(output_tasks.items(), key=lambda x: x[1])

            output_str = "刪除成功!!\nTask:"

            for i in range(0, len(output_tasks)):
                output_str += ("\n"+str(i+1)+". "+str(output_tasks[i][0]))
            print(output_tasks)

            # 七天後到期
            self.r.expire(uid, 60*60*24*7)

            # 送出res
            send_text_message(reply_token, output_str)
            self.go_back()

    def on_exit_delete_state(self):

        print("Leaving delete_state")

    def on_enter_update_state(self, event):  # 改 old_task new_task

        print("I'm entering update_state")

        # 從event抓資料

        text = event.message.text

        reply_token = event.reply_token

        uid = event.source.user_id

        try:
            # 字串處理
            text = text[1:]
            text = str(text).strip(" ")
            tasks = text.split(" ")

            # 修改對應task內容

            if(len(tasks) >= 2):
                old_task = tasks[0]
                new_task = tasks[1]

                if self.r.hexists(uid,old_task):
                    pipe=self.r.pipeline()
                    timestamp = self.r.hget(uid,old_task)
                    self.r.hdel(uid,old_task)
                    self.r.hset(uid,old_task,timestamp)
                    pipe.execute()
        except:
            pass
        finally:
            # 打印tasks
            output_tasks = self.r.hgetall(uid)
            output_tasks = sorted(self.r[uid].items(), key=lambda x: x[1])
            output_str = "修改成功!!\nTask:"

            for i in range(0, len(output_tasks)):
                output_str += ("\n"+str(i+1)+". "+str(output_tasks[i][0]))
            print(output_tasks)

            # 七天後到期
            self.r.expire(uid, 60*60*24*7)

            # 送出res
            send_text_message(reply_token, output_str)
            self.go_back()

    def on_exit_update_state(self):

        print("Leaving update_state")

    def on_enter_sunrise_state(self, event):  # 日出

        print("I'm entering sunrise_state")

        # 從event抓資料

        reply_token = event.reply_token

        uid = event.source.user_id

        try:
            # 爬日出時間
            sunrise_times = crawler.fetch_sun_time()

            output_str = "查詢成功!!\n日出時間:"

            output_str += ("\n今天: "+str(sunrise_times[0]))

            output_str += ("\n明天: "+str(sunrise_times[2]))

            send_text_message(reply_token, output_str)
        except:
            pass
        finally:
            self.go_back()

    def on_exit_sunrise_state(self):

        print("Leaving sunrise_state")

    def on_enter_explain_state(self, event):  # 解說指令

        print("I'm entering explain_state")

        self.go_back()

    def on_exit_explain_state(self):

        print("Leaving explain_state")

    def on_enter_sunset_state(self, event):  # 日落

        print("I'm entering sunset_state")

        # 從event抓資料

        reply_token = event.reply_token

        uid = event.source.user_id
        try:
            # 爬日出時間

            sundown_times = crawler.fetch_sun_time()

            output_str = "查詢成功!!\n日落時間:"

            output_str += ("\n今天: "+str(sundown_times[1]))

            output_str += ("\n明天: "+str(sundown_times[3]))

            send_text_message(reply_token, output_str)
        except:
            pass
        finally:
            self.go_back()

    def on_exit_sunset_state(self):

        print("Leaving sunset_state")

    def on_enter_FSM_state(self, event):  # FSM

        print("I'm entering FSM_state")

        reply_token = event.reply_token

        HOST_IP = os.environ.get("HOST_NAME", "0.0.0.1")

        try:
            send_image_url(reply_token, HOST_IP+"/show-fsm")
        except:
            pass
        finally:
            self.go_back()

    def on_exit_FSM_state(self):

        print("Leaving FSM_state")

    def on_enter_murmur_state(self, event):  # 可憐啊

        print("I'm entering murmur_state")

        reply_token = event.reply_token

        try:
            send_image_url(
                reply_token, "https://memeprod.sgp1.digitaloceanspaces.com/meme/a9a16134b16c3a8d71fbd3ea723f9efe.png")
        except:
            pass
        finally:
            self.go_back()

    def on_exit_murmur_state(self):

        print("Leaving murmur_state")
