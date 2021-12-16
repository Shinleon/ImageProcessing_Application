import tkinter as tk
from tkinter.messagebox import showinfo

import Constants as CONST
from custom_log import print_log


class HistoryFrame(tk.Frame):
    def __init__(self, parent, app_state, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.app_state = app_state

        def add_history():
            parent.add_to_history()

        def remove_history():
            selected_indices = self.list_box.curselection()
            if len(selected_indices) != 1:
                return
            print_log(f"selected_indices: {selected_indices}")
            self.app_state[CONST.HISTORY] = self.app_state[CONST.HISTORY][
                0 : selected_indices[0]
            ]
            self.list_box.clear()
            for item in self.app_state[CONST.HISTORY]:
                self.add_history(item)
                self.app_state[CONST.ARR][CONST.ORIGINAL_IMG] = item[-1]
            if len(self.app_state[CONST.HISTORY]) == 0:
                self.app_state[CONST.ARR][CONST.ORIGINAL_IMG] = self.app_state[
                    CONST.ORIGINAL_IMG
                ]
                self.app_state[CONST.ARR][CONST.MODIFIED_IMG] = self.app_state[
                    CONST.ORIGINAL_IMG
                ]
            self.parent.rerender()

        self.add_button = tk.Button(
            self, text="add to history", bg="purple", fg="blue", command=add_history
        )
        self.add_button.pack(side=tk.TOP, fill="none", expand=0)

        self.remove_button = tk.Button(
            self,
            text="remove from history",
            bg="purple",
            fg="blue",
            command=remove_history,
        )
        self.remove_button.pack(side=tk.TOP, fill="none", expand=0)

        action_var = tk.StringVar(value=app_state[CONST.HISTORY])
        self.list_box = HistoryList(
            self,
            listvariable=action_var,
            height=10,
            selectmode=tk.SINGLE,
            fg="black",
            bg="cyan",
        )
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.list_box.yview)
        self.list_box["yscrollcommand"] = scrollbar.set

        # def items_selected(event):
        #     """handle item selected event"""
        #     # get selected indices
        #     selected_indices = self.list_box.curselection()
        #     # get selected items
        #     selected_action = ",".join([self.list_box.get(i) for i in selected_indices])
        #     msg = f"You selected: {selected_action}"

        #     showinfo(title="Information", message=msg)

        # self.list_box.bind("<<ListboxSelect>>", items_selected)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_box.pack(side=tk.TOP, fill="none")

    def add_history(self, history_log):
        self.list_box.insert(tk.END, f"{history_log[0]} {history_log[1]} ")


class HistoryList(tk.Listbox):
    def __init__(self, parent, *args, **kwargs):
        tk.Listbox.__init__(self, parent, *args, **kwargs)

    def clear(self):
        self.delete(0, tk.END)
