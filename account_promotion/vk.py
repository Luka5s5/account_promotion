import vk_api
from time import sleep
import time

class vk_collection:
    sessions=[]
    ind=0
    sleep_t=0
    custom_t=False
    tasks=[]   
    size_limit=25 
    def __init__(self,**kwargs): 
        with open('temp/data.txt','r') as f:
            print('initing vk accounts')
            for line in f:
                login,password = line.split()
                print('initing '+login)
                self.sessions.append(vk_api.VkApi(login=login,password=password)) # ,app_id=2685278
                # captcha case
                # captcha = vk_api.Captcha(self.sessions[-1], str(int(time.time())), login)
                # self.sessions[-1].error_handlers[vk_api.CAPTCHA_ERROR_CODE](captcha)
                print(self.sessions[-1].check_sid())
                self.sessions[-1].auth(token_only=True) 
            print('done initing vk accounts')
        if('sleep' in kwargs):
            self.sleep_t=kwargs['sleep']
            self.custom_t=True
        else:
            self.sleep_t=0.4/len(self.sessions)
    def get_session(self):
        if (len(self.sessions) == 0):
            print("No more sessions")
            quit()
        self.ind+=1
        self.ind%=len(self.sessions)
        return self.sessions[self.ind]

    def change_session(self):
        del self.sessions[self.ind] #get_session увеличила ind
        if len(self.sessions) == 0:
            print("No more sessions")
            quit()
        if not self.custom_t:
            self.sleep_t=0.4/len(self.sessions)
        self.ind%=len(self.sessions)

    def execute_callbacks(self, response):
        size = len(self.tasks)
        for i in range(len(self.tasks)):
            if (isinstance(response[i], bool) and not response[i]):
                size -= 1
        if (size == 0):
            print("Error while huge request, changing session and skipping all request")
            self.change_session()
            return
        
        for i in range(len(self.tasks)):
            if (isinstance(response[i], bool) and not response[i]):
                continue
            self.tasks[i][2](response[i], **self.tasks[i][3]) # calling a callback

    def execute_tasks(self):
        if(self.sleep_t!=0):
            sleep(self.sleep_t)
        if (len(self.tasks) == 0):
            return
        print("LOG: executing " + str(len(self.tasks)) + " tasks")
        code = "return ["
        for task in self.tasks:
            code += "API." + task[0] + "(" + str(task[1]) + "), " 
        code = code[:-2]
        code += "];"
        self.direct_call("execute",
                        {"code": code},
                        self.execute_callbacks,
        )
        print("LOG: executed, now processing...")
            
    def add_task(self, method, method_args, callback, **kwargs):
        self.tasks += [(method, method_args, callback, kwargs)]
        if (len(self.tasks) == self.size_limit):
            self.execute_tasks()
            self.tasks = [] 

    def direct_call(self,method,method_args,callback,**kwargs):
        if(self.sleep_t!=0):
            sleep(self.sleep_t)
        while(True):
            try:
                return callback(self.get_session().method(method,values=method_args), **kwargs)
            except Exception as ex:
                try:
                    print(ex.error['error_msg'], ex.code)
                    VK_error = True
                except Exception as ex1:
                    VK_error = False
                if(VK_error and ex.code in (29,6,14,)):
                    print("LOG: Changing session")
                    self.change_session()                    
                else:
                    print("LOG: Skip the request")
                    return None
