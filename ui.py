import gi
import sys

#sys.path.insert(0, "/home/jslin/Projects/jslinpwd")

import jslinpwd

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class PwdWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="jslinpwd")
        self.set_border_width(10)
        self.set_default_size(200,400)
        self.pwds = jslinpwd.init()
        self.selectedsite = None
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        # Setting up the self.grid in which the elements are to be positioned
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Creating the ListStore model
        self.site_liststore = Gtk.ListStore(str)
        for site in self.pwds:
            self.site_liststore.append([site])

        self.treeview = Gtk.TreeView(model=self.site_liststore)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Sites", renderer, text=0)
        self.treeview.append_column(column)
        self.select = self.treeview.get_selection()
        self.select.connect("changed", self.on_tree_selection_changed)

        self.copybutton = Gtk.Button(label="Copy")
        self.copybutton.connect("clicked", self.on_copy_button_clicked)
        self.buttons = list()


        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(
            self.copybutton, self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1
        )

        self.scrollable_treelist.add(self.treeview)

#         icontheme = Gtk.IconTheme.get_default()
#         self.icon = icontheme.load_icon(Gtk.STOCK_FLOPPY, 48, 0)
#         self.set_icon(self.icon)

        self.show_all()

    def on_copy_button_clicked(self, widget):
        if self.selectedsite != None:
            self.clipboard.set_text(self.pwds[self.selectedsite].strip(), -1)

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.selectedsite = model[treeiter][0]
            # print("You selected", model[treeiter][0])
        else:
            self.selectedsite = None

if __name__ == '__main__':
    
    win = PwdWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
