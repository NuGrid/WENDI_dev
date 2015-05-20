import widget_framework as framework
from IPython.html import widgets
from IPython.display import display, clear_output
from matplotlib import pyplot
import nugridse as mp
import mesa as ms


frame = framework.framework()
frame.set_default_display_style(padding="0.25em",background_color="white", border_color="LightGrey", border_radius="0.5em")
frame.set_default_io_style(padding="0.25em", margin="0.25em", border_color="LightGrey", border_radius="0.5em")


states_movie = ["movie", "movie_iso_abund", "movie_abu_chart"]
states_nugrid = ["nugrid", "nugrid_w_data", "iso_abund", "abu_chart"]+states_movie
states_mesa = ["mesa", "mesa_w_data", "hrd", "plot"]
states_plotting = states_nugrid[2:]+states_mesa[2:]

frame.add_state(states_nugrid)
frame.add_state(states_mesa)

frame.add_display_object("window")
frame.add_io_object("Title")
frame.add_display_object("widget")

###Data page###
frame.add_display_object("page_data")
frame.add_io_object("mass")
frame.add_io_object("Z")
frame.add_io_object("select_nugrid_mesa")

frame.add_display_object("contain_module_load")
frame.add_io_object("select_module")
frame.add_io_object("load_data")

frame.add_io_object("select_plot")

frame.set_state_children("window", ["Title", "widget"])
frame.set_state_children("widget", ["page_data"], titles=["Data"])
frame.set_state_children("page_data", ["mass", "Z", "select_nugrid_mesa",
                                       "contain_module_load", "select_plot"])
frame.set_state_children("contain_module_load", ["select_module", "load_data"])

###Plotting page###
frame.add_display_object("page_plotting")

frame.add_io_object("warning_msg")

frame.add_io_object("plot_name")
frame.add_io_object("cycle")
frame.add_io_object("cycle_range")
frame.add_io_object("movie_type")

frame.add_display_object("xax")
frame.add_io_object("xaxis")
frame.add_io_object("logx")
frame.add_display_object("yax")
frame.add_io_object("yaxis")
frame.add_io_object("logy")

frame.add_display_object("mass_settings")
frame.add_io_object("set_amass")
frame.add_io_object("amass_range")
frame.add_io_object("set_mass")
frame.add_io_object("mass_range")
frame.add_io_object("lbound")

frame.add_display_object("lim_settings")
frame.add_io_object("set_lims")
frame.add_io_object("ylim")
frame.add_io_object("xlim")

frame.add_io_object("stable")

frame.add_display_object("abu_settings")
frame.add_io_object("ilabel")
frame.add_io_object("imlabel")
frame.add_io_object("imagic")

frame.add_io_object("generate_plot")

frame.set_state_children("widget", ["page_plotting"], titles=["Plotting"])
frame.set_state_children("page_plotting", ["warning_msg", "plot_name", "movie_type", "cycle", "cycle_range",
                                           "xax", "yax", "stable", "mass_settings",
                                           "lim_settings", "abu_settings", "stable", "generate_plot"])
frame.set_state_children("xax", ["xaxis", "logx"])
frame.set_state_children("yax", ["yaxis", "logy"])
frame.set_state_children("mass_settings", ["set_amass", "amass_range", "set_mass", "mass_range",
                                           "lbound"])
frame.set_state_children("lim_settings", ["set_lims", "xlim", "ylim"])
frame.set_state_children("abu_settings", ["ilabel", "imlabel", "imagic"])


###DEFAULT###

frame.set_state_data("class_instance", None)

frame.set_state_attribute('window', visible=True, border_style="", border_radius="0em")
frame.set_state_attribute('Title', visible=True, value = "<h1>NuGrid / Mesa Explorer</h1>")
frame.set_state_attribute('widget', visible=True, border_style="", border_radius="0em")

frame.set_state_attribute("page_data", visible=True)
frame.set_state_attribute('mass', visible=True, description="Mass: ", options=["1.0", "1.65", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "12.0", "15.0", "20.0", "25.0", "32.0", "60.0"], selected_label="2.0")
frame.set_state_attribute('Z', visible=True, description="Z: ",
                          options=["1E-4", "1E-3", "6E-3", "1E-2", "2E-2"])
frame.set_state_attribute("select_nugrid_mesa", visible=True,
                          description="Select NuGrid or Mesa: ",
                          options=["", "NuGrid", "Mesa"])
frame.set_state_attribute("contain_module_load", visible=True, border_style="", border_radius="0em")
frame.set_state_attribute("select_module", visible=True,
                          description="Select data type: ", disabled=True)
frame.set_state_attribute("load_data", visible=True,
                          description="Load Data", disabled=True)
frame.set_state_attribute("select_plot", visible=True,
                          description="Select plot type: ", disabled=True)

###NUGRID###
frame.set_state_attribute("select_module", states_nugrid, options=["", "H5 out"], disabled=False)
frame.set_state_attribute("load_data", states_nugrid, disabled=False)
frame.set_state_attribute("select_plot", states_nugrid[1:], options={"":"nugrid_w_data", "Isotope abundance":"iso_abund", "Abundance chart":"abu_chart", "Movie":"movie"}, disabled=False)

###MESA###
frame.set_state_attribute("select_module", states_mesa, options=["", "History", "Profile"], disabled=False)
frame.set_state_attribute("load_data", states_mesa, disabled=False)
frame.set_state_attribute("select_plot", states_mesa[1:], options={"":"mesa_w_data", "HR-Diagram":"hrd", "Plot":"plot"}, disabled=False)

###CALLBACKS###
def sel_nugrid_mesa(widget, value):
    if value=="NuGrid":
        frame.set_state("nugrid")
    elif value=="Mesa":
        frame.set_state("mesa")
    elif value=="":
        frame.set_state("default")

def load(widget):
    clear_output()
    data = None
    mass = float(frame.get_attribute("mass", "value"))
    Z = float(frame.get_attribute("Z", "value"))
    module = frame.get_attribute("select_module", "value")
    if module == "H5 out":
        data = mp.se(mass=mass, Z=Z)
        frame.set_state("nugrid_w_data")
    elif module == "History":
        data = ms.history_data(mass=mass, Z=Z)
        frame.set_state("mesa_w_data")
        frame.set_attributes("xaxis", options=data.cols.keys())
        frame.set_attributes("yaxis", options=data.cols.keys())
    elif module == "Profile":
        data = ms.mesa_profile(mass=mass, Z=Z)
        frame.set_state("mesa_w_data")
        frame.set_attributes("xaxis", options=data.cols.keys())
        frame.set_attributes("yaxis", options=data.cols.keys())
    else:
        frame.set_state("default")
    frame.set_state_data("class_instance", data)
    frame.set_attributes("select_plot", selected_label="")
    
        
def sel_plot(widget, value):
    data = frame.get_state_data("class_instance")
    
    if value in ["iso_abund", "abu_chart"]:
        cycle_list = data.se.cycles
        step = int(cycle_list[1])-int(cycle_list[0])
        min = int(cycle_list[0])
        max = int(cycle_list[-1])
        
        mass_list = data.se.get(min, "mass")
        mass_min, mass_max = mass_list[0], mass_list[-1]
        mass_step = (mass_max - mass_min)/200.0
        frame.set_state_attribute("mass_range", ["iso_abund", "abu_chart"], min=mass_min, max=mass_max,
                                  value=(mass_min, mass_max), step=mass_step)
        
        frame.set_state_attribute('cycle', ["iso_abund", "abu_chart"], min=min, max=max, step=step)
        
    frame.set_state(value)
    
def change_module(widget, value):
    if value == "History":
        frame.set_state_attribute("select_plot", states_mesa[1:], options={"":"mesa_w_data", "HR-Diagram":"hrd", "Plot":"plot"})
    elif value == "Profile":
        frame.set_state_attribute("select_plot", states_mesa[1:], options={"":"mesa_w_data", "Plot":"plot"})

frame.set_state_callbacks("select_nugrid_mesa", sel_nugrid_mesa)
frame.set_state_callbacks("select_module", change_module)
frame.set_state_callbacks("load_data", load, attribute=None, type="on_click")
frame.set_state_callbacks("select_plot", sel_plot)

frame.set_object("window", widgets.Box())
frame.set_object("Title", widgets.HTML())
frame.set_object("widget", widgets.Tab())

frame.set_object("page_data", widgets.VBox())
frame.set_object("mass", widgets.Dropdown(options=["2.0"]))#The option 2.0 is defined since above the selected_label is defined as 2.0, and selected_label is set before options causing a key error
frame.set_object("Z", widgets.ToggleButtons())

frame.set_object("select_nugrid_mesa", widgets.Dropdown())
frame.set_object("contain_module_load", widgets.HBox())
frame.set_object("select_module", widgets.Dropdown())
frame.set_object("load_data", widgets.Button())
frame.set_object("select_plot", widgets.Dropdown())


###Plotting page###
frame.set_state_attribute('page_plotting', visible=True)

frame.set_state_attribute('warning_msg', visible=True, value="<h3>Error: No data loaded!</h3>")
frame.set_state_attribute("warning_msg", ["nugrid_w_data", "mesa_w_data"], value="<h3>Error: No plot selected!</h3>")
frame.set_state_attribute("warning_msg", states_plotting, visible=False)

frame.set_state_attribute("plot_name", border_style="", border_radius="0em")
frame.set_state_attribute('plot_name', "iso_abund", visible=True, value="<h2>Isotope abundance</h2>")
frame.set_state_attribute('plot_name', "abu_chart", visible=True, value="<h2>Abundance chart</h2>")
frame.set_state_attribute('plot_name', states_movie, visible=True, value="<h2>Movie</h2>")
frame.set_state_attribute('plot_name', "hrd", visible=True, value="<h2>HR-Diagram</h2>")
frame.set_state_attribute('plot_name', "plot", visible=True, value="<h2>Plot</h2>")

frame.set_state_attribute('movie_type', states_movie, visible=True, description="Movie Type: ", options={"":"movie", "Isotope abundance":"movie_iso_abund", "Abundance chart":"movie_abu_chart"})
frame.set_state_attribute('cycle', ["iso_abund", "abu_chart"], visible=True, description="cycle: ")
frame.set_state_attribute('cycle_range', states_movie, visible=True)

frame.set_state_attribute('xax', "plot", visible=True, border_style="", border_radius="0em")
frame.set_state_attribute('xaxis', visible=True, description="select X-axis: ")
frame.set_state_attribute('logx', visible=True, description="log X-axis: ")
frame.set_state_attribute('yax', "plot", visible=True, border_style="", border_radius="0em")
frame.set_state_attribute('yaxis', visible=True, description="select Y-axis: ")
frame.set_state_attribute('logy', visible=True, description="log Y-axis: ")

frame.set_state_attribute("mass_settings", ["iso_abund", "abu_chart"]+states_movie[1:], visible=True, border_style="", border_radius="0em")
frame.set_state_attribute("set_amass", ["iso_abund", "movie_iso_abund"], visible=True, description="Set atomic mass: ")
frame.set_state_attribute("amass_range", ["iso_abund", "movie_iso_abund"], description="Atomi mass range: ", min=0, max=211, value=(0, 211))
frame.set_state_attribute("set_mass", ["iso_abund", "abu_chart"]+states_movie[1:], visible=True, description="Set mass: ")
frame.set_state_attribute("mass_range", ["iso_abund", "abu_chart"]+states_movie[1:], description="Mass range: ")
frame.set_state_attribute("lbound", "abu_chart", visible=True, description="lbound", min=-12, max=0, step=0.05, value=(-12, 0))
frame.set_state_attribute("lbound", min=-12, max=0)#make sure the limits are set before the value

frame.set_state_links("amass_link", [("set_amass", "value"), ("amass_range", "visible")], ["iso_abund", "movie_iso_abund"], True)
frame.set_state_links("mass_link", [("set_mass", "value"), ("mass_range", "visible")], ["iso_abund", "abu_chart"]+states_movie[1:], True)

frame.set_state_attribute("lim_settings" , ["iso_abund", "abu_chart"]+states_movie[1:], visible=True, border_style="", border_radius="0em")
frame.set_state_attribute("set_lims", ["iso_abund", "abu_chart"]+states_movie[1:], visible=True, description="Set axis limits: ")
frame.set_state_attribute("xlim", ["abu_chart", "movie_abu_chart"], description="x-axis limits: ", min=0, max=130, value=(0, 130), step=0.5)
frame.set_state_attribute("ylim", ["iso_abund", "abu_chart"]+states_movie[1:], description="y-axis limits: ")
frame.set_state_attribute("ylim", ["iso_abund", "movie_iso_abund"], min=-13, max=0, step=0.05, value=(-13, 0))
frame.set_state_attribute("ylim", min=-13, max=0)#make sure the limits are set before the value
frame.set_state_attribute("ylim", ["abu_chart", "movie_abu_chart"], min=0, max=130, value=(0, 130), step=0.5)

frame.set_state_links("xlims_link", [("set_lims", "value"), ("xlim", "visible")], ["abu_chart", "movie_abu_chart"], True)
frame.set_state_links("ylims_link", [("set_lims", "value"), ("ylim", "visible")], ["iso_abund", "abu_chart"]+states_movie[1:], True) 

frame.set_state_attribute("abu_settings", ["abu_chart", "movie_abu_chart"], visible=True, border_style="", border_radius="0em")
frame.set_state_attribute("ilabel", ["abu_chart", "movie_abu_chart"], visible=True, description="Element label")
frame.set_state_attribute("imlabel", ["abu_chart", "movie_abu_chart"], visible=True, description="Isotope label")
frame.set_state_attribute("imagic", ["abu_chart", "movie_abu_chart"], visible=True, description="Magic numbers")

frame.set_state_attribute("stable", "iso_abund", visible=True, description="stable: ")

frame.set_state_attribute('generate_plot', states_plotting, visible=True, description="Generate Plot", font_size="1.25em", font_weight="bold")
        
def sel_movie_plot(widget, value):
    data = frame.get_state_data("class_instance")
    
    if value in ["movie_iso_abund", "movie_abu_chart"]:
        cycle_list = data.se.cycles
        step = int(cycle_list[1])-int(cycle_list[0])
        min = int(cycle_list[0])
        max = int(cycle_list[-1])
        
        mass_list = data.se.get(min, "mass")
        mass_min, mass_max = mass_list[0], mass_list[-1]
        mass_step = (mass_max - mass_min)/200.0
        frame.set_state_attribute("mass_range", ["movie_iso_abund", "movie_abu_chart"], min=mass_min, max=mass_max,
                                  value=(mass_min, mass_max), step=mass_step)
        
        frame.set_state_attribute('cycle_range', ["movie_iso_abund", "movie_abu_chart"], min=min, max=max, step=step, value=(min, max))
        
    frame.set_state(value)

def make_plot(widget):
    clear_output()
    pyplot.close("all")
    state = frame.get_state()
    
    data = frame.get_state_data("class_instance")
    cycle = frame.get_attribute("cycle", "value")
    cycle_range = frame.get_attribute("cycle_range", "value")
    xax = frame.get_attribute("xaxis", "value")
    logx = frame.get_attribute("logx", "value")
    yax = frame.get_attribute("yaxis", "value")
    logy = frame.get_attribute("logy", "value")
    if frame.get_attribute("set_amass", "value"):
        amass = frame.get_attribute("amass_range", "value")
        amass = [amass[0], amass[1]]
    else:
        amass = None
        
    if frame.get_attribute("set_mass", "value"):
        mass = frame.get_attribute("mass_range", "value")
        mass = [mass[0], mass[1]]
    else:
        mass = None
        
    lbound = frame.get_attribute("lbound", "value")
        
    if frame.get_attribute("set_lims", "value"):
        xlim = frame.get_attribute("xlim", "value")
        ylim = frame.get_attribute("ylim", "value")
    else:
        xlim = [0, 0]
        ylim = [0, 0]
        
    stable = frame.get_attribute("stable", "value")
    ilabel = frame.get_attribute("ilabel", "value")
    imlabel = frame.get_attribute("imlabel", "value")
    imagic = frame.get_attribute("imagic", "value")
        
    if state=="iso_abund":
        data.iso_abund(cycle, stable, amass, mass, ylim)
    elif state=="abu_chart":
        plotaxis = [xlim[0], xlim[1], ylim[0], ylim[1]]
        data.abu_chart(cycle, mass, ilabel, imlabel, imagic=imagic, lbound=lbound, plotaxis=plotaxis, ifig=1)
    elif state=="plot":
        print xax, yax
        data.plot(xax, yax, logx=logx, logy=logy)
    elif state=="hrd":
        data.hrd_new()
    elif state=="movie_iso_abund":
        cycles = data.se.cycles
        cyc_min = cycles.index("%010d" % (cycle_range[0], ))
        cyc_max = cycles.index("%010d" % (cycle_range[1], ))
        cycles = cycles[cyc_min:cyc_max]
        display(data.movie(cycles, "iso_abund", amass_range=amass, mass_range=mass, ylim=ylim))
    elif state=="movie_abu_chart":
        cycles = data.se.cycles
        cyc_min = cycles.index("%010d" % (cycle_range[0], ))
        cyc_max = cycles.index("%010d" % (cycle_range[1], ))
        cycles = cycles[cyc_min:cyc_max]
        plotaxis = [xlim[0], xlim[1], ylim[0], ylim[1]]
        display(data.movie(cycles, "abu_chart", mass_range=mass, ilabel=ilabel, imlabel=imlabel, imagic=imagic, plotaxis=plotaxis))


frame.set_state_callbacks("movie_type", sel_movie_plot)
frame.set_state_callbacks("generate_plot", make_plot, attribute=None, type="on_click")

frame.set_object("page_plotting", widgets.VBox())
frame.set_object("warning_msg", widgets.HTML())
frame.set_object("plot_name", widgets.HTML())
frame.set_object("movie_type", widgets.Dropdown())
frame.set_object("cycle", widgets.IntSlider())
frame.set_object("cycle_range", widgets.IntRangeSlider())
frame.set_object("xax", widgets.HBox())
frame.set_object("xaxis", widgets.Select())
frame.set_object("logx", widgets.Checkbox())
frame.set_object("yax", widgets.HBox())
frame.set_object("yaxis", widgets.Select())
frame.set_object("logy", widgets.Checkbox())

frame.set_object("mass_settings", widgets.VBox())
frame.set_object("set_amass", widgets.Checkbox())
frame.set_object("amass_range", widgets.IntRangeSlider())
frame.set_object("set_mass", widgets.Checkbox())
frame.set_object("mass_range", widgets.FloatRangeSlider())
frame.set_object("lbound", widgets.FloatRangeSlider())

frame.set_object("lim_settings", widgets.VBox())
frame.set_object("set_lims", widgets.Checkbox())
frame.set_object("ylim", widgets.FloatRangeSlider())
frame.set_object("xlim", widgets.FloatRangeSlider())

frame.set_object("stable", widgets.Checkbox())

frame.set_object("abu_settings", widgets.HBox())
frame.set_object("ilabel", widgets.Checkbox())
frame.set_object("imlabel", widgets.Checkbox())
frame.set_object("imagic", widgets.Checkbox())

frame.set_object("generate_plot", widgets.Button())


def start_explorer():
    frame.display_object("window")