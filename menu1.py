from Tkinter import *

################################################################
root = Tk()

class ConfigParamStruct():
    def __init__(self, name, var):
        self.name = name
        if type(var) == str:
            self.var = StringVar()
        else:
            self.var = IntVar()

        self.var.set(var)

class ModuleBox():
    def __init__(self, module_name, positional_index, config_params = []):
        self.module_enabled = IntVar()
        self.config_params  = []
        self.config_param_states = []
        self.module_enabled.set(1)

        _module_lf = LabelFrame(root, text=module_name)
        _config_lf = LabelFrame(_module_lf, text=module_name + ' Config')
        _module_cb = Checkbutton(_module_lf, text=module_name, variable=self.module_enabled, command=self.cb_state)

        _module_lf.grid(row=0, column=positional_index + 2 if positional_index > 0 else positional_index, sticky=N)
        _config_lf.grid(row=1, column=positional_index + 3 if positional_index > 0 else positional_index + 1)
        _module_cb.grid(row=0, column=0)

        for i, param in enumerate(config_params):
            self.config_param_states.append(IntVar() if type(param.var.get()) != str else StringVar())
            self.config_param_states[-1].set(param.var.get())

            if type(param.var.get()) == str:
                self.config_params.append(Label(_config_lf, text=param.name))
                self.config_params[-1].grid(row=i, column=1, sticky=E)
                self.config_params.append(Entry(_config_lf, textvariable=self.config_param_states[-1]))
            else:
                self.config_params.append(Checkbutton(_config_lf, text=param.name, variable=self.config_param_states[-1]))

            self.config_params[-1].grid(row=i, column=0, sticky=W)

    def cb_state(self):
        if self.module_enabled.get():
            for param in self.config_params:
                param.config(state=NORMAL)
        else:
            for param in self.config_params:
                param.config(state=DISABLED)

def main():
    ModuleBox("Drivers", 0, [
                                ConfigParamStruct("test1", 0),
                                ConfigParamStruct("test2", "beepboop"),
                                ConfigParamStruct("test3", 1),
                                ConfigParamStruct("test4", "Zipzop"),
                                ConfigParamStruct("test5", 1)
                            ]
             )

    ModuleBox("Events", 1, [
                                ConfigParamStruct("test1", "zoopdop"),
                                ConfigParamStruct("test2", 1),
                                ConfigParamStruct("test3", 0),
                                ConfigParamStruct("test4", 1)
                            ]
             )

    ModuleBox("RTOS", 2, [
                                ConfigParamStruct("test1", "rtos1"),
                                ConfigParamStruct("test2", 1),
                                ConfigParamStruct("test3", 0),
                                ConfigParamStruct("test4", 1),
                                ConfigParamStruct("test5", 1),
                                ConfigParamStruct("test6", 0),
                                ConfigParamStruct("test7", 0),
                                ConfigParamStruct("test8", 0),
                                ConfigParamStruct("test9", 1),
                                ConfigParamStruct("test10", "115200"),
                                ConfigParamStruct("test11", "rtos3"),
                            ]
             )

    ModuleBox("Platform", 4, [
                                ConfigParamStruct("test1", 1),
                                ConfigParamStruct("test2", 0),
                                ConfigParamStruct("test3", 1),
                                ConfigParamStruct("test4", 0),
                                ConfigParamStruct("test5", 0),
                            ]
             )

    root.mainloop()


if __name__ == '__main__':
    main()
