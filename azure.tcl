
package require Ttk
namespace eval ttk::theme::azure {
    variable colors
    array set colors {
        -accent "#0078D7"
        -bg "#333333"
        -fg "#F0F0F0"
        -button-fg "#F0F0F0"
        -button-bg "#4A4A4A"
        -button-active-bg "#5A5A5A"
        -entry-bg "#3E3E3E"
        -entry-fg "#F0F0F0"
        -border "#555555"
        -disabled-fg "#777777"
    }

    proc load_theme {name} {
        variable colors
        set C $colors
        ttk::style theme create $name -parent clam -settings {
            ttk::style configure . -background $C(-bg) -foreground $C(-fg) -troughcolor $C(-bg) -bordercolor $C(-border) -font {Segoe UI} 10
            ttk::style configure TButton -background $C(-button-bg) -foreground $C(-button-fg) -borderwidth 0 -padding {10 5}
            ttk::style map TButton -background [list active $C(-button-active-bg)] -foreground [list disabled $C(-disabled-fg)]
            ttk::style configure TEntry -fieldbackground $C(-entry-bg) -foreground $C(-entry-fg) -insertcolor $C(-entry-fg) -borderwidth 1
            ttk::style configure Treeview -background $C(-entry-bg) -fieldbackground $C(-entry-bg) -foreground $C(-fg)
            ttk::style map Treeview -background [list selected $C(-accent)]
            ttk::style configure Treeview.Heading -background $C(-button-bg) -foreground $C(-button-fg) -font {Segoe UI} 10 bold -padding 5
        }
    }
}
package provide ttk::theme::azure 1.0
    