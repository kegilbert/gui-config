import json
import sys
import glob
import fnmatch
import os

if sys.version_info[0] >= 3:
    from tkinter import *
else:
    from Tkinter import *

################################################################
root = Tk()
help_text = StringVar()
help_box = Label(root, textvariable=help_text, wraplength=750, justify=LEFT)
modules = []

class ConfigParamStruct():
    def __init__(self, name, var, help):
        self.name = name
        self.help = help
        self.var  = var

class ModuleBox():
    def __init__(self, module_name, positional_index, config_params = []):
        self.module_enabled = IntVar()
        self.config_params  = []
        self.config_param_states = []
        self.config_param_init_states = []
        self.module_enabled.set(1)

        _module_lf = LabelFrame(root, text=module_name)
        _config_lf = LabelFrame(_module_lf, text=module_name + ' config')
        _module_cb = Checkbutton(_module_lf, text=module_name, variable=self.module_enabled, command=self.cb_state)

        _module_lf.grid(row=0, column=positional_index + 2 if positional_index > 0 else positional_index, sticky=N)
        _config_lf.grid(row=1, column=positional_index + 3 if positional_index > 0 else positional_index + 1)
        _module_cb.grid(row=0, column=0)

        for i, param in enumerate(config_params):
            if type(param.var) == str:
                self.config_param_states.append(StringVar())
                self.config_param_init_states.append(StringVar())
            elif type(param.var) == int:
                self.config_param_states.append(IntVar())
                self.config_param_init_states.append(IntVar())
            else:
                self.config_param_states.append(BooleanVar())
                self.config_param_init_states.append(BooleanVar())

            self.config_param_states[-1].set(param.var)
            self.config_param_init_states[-1].set(param.var)

            format = type(param.var)

            if (format == str or format == int):
                self.config_params.append({'widget': Label(_config_lf, text=param.name), 'help': param.help})
                self.config_params[-1]['widget'].grid(row=i, column=1, sticky=E)
                self.config_params.append({'widget': Entry(_config_lf, textvariable=self.config_param_states[-1]), 'help': param.help})
            else:
                self.config_params.append({'widget': Checkbutton(_config_lf, text=param.name, variable=self.config_param_states[-1]), 'help': param.help})

            self.config_params[-1]['widget'].bind("<Enter>", self.on_enter)
            self.config_params[-1]['widget'].grid(row=i, column=0, sticky=W)

    def get_state_diff(self):
        diff = []
        for i, state in enumerate(self.config_param_init_states):
            if state.get() != self.config_param_states[i].get():
                diff.append(self.config_params[i]['widget'].cget('text'))

        print(diff)

    def on_enter(self, event):
        for widget in self.config_params:
            if widget['widget'] == event.widget:
                help_text.set(widget['help'])

    def cb_state(self):
        if self.module_enabled.get():
            for param in self.config_params:
                param['widget'].config(state=NORMAL)
        else:
            for param in self.config_params:
                param['widget'].config(state=DISABLED)

def save_config():
    print("Saving config")
    for mod in modules:
        mod.get_state_diff()

def main():
    if sys.version_info[0] >= 3:
        for filename in glob.iglob('./**/mbed_lib.json', recursive=True):
            print(filename)

    module_paths = ['platform/mbed_lib.json', 'drivers/mbed_lib.json', 'events/mbed_lib.json', 'rtos/mbed_lib.json']

    if os.path.isfile('mbed_app.json'):
        module_paths.append('mbed_app.json')

    help_box.grid(row=99, column=0, sticky=S, columnspan = 6)

    for i, mod in enumerate(module_paths):
        f = open(mod, 'r')
        config = json.loads(f.read()).get('config')
        f.close()
        parameters = []
        config_iteritems = {}

        if sys.version_info[0] < 3:
            config_iteritems = config.iteritems()
        else:
            config_iteritems = config.items()

        for key, value in config_iteritems:
            try:
                parameters.append(ConfigParamStruct(key, value.get('value'), value.get('help')))
            except AttributeError:
                parameters.append(ConfigParamStruct(key, True if value else False, "Enable/Disable this module"))  # present flag

        modules.append(ModuleBox(mod[0:-14], i, parameters))


    save_button = Button(root, text="Save", width=12, height=2, bg="green", activebackground="darkgreen", command=save_config)
    save_button.grid(row=99, column=99, sticky=NW)

    root.mainloop()


if __name__ == '__main__':
    main()
