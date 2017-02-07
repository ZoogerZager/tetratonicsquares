from collections import OrderedDict
from pygame import midi
from tkinter import *
from tkinter import ttk

class tetratonicsquares:

    midi.init()
    player = midi.Output(0)
    player.set_instrument(10, 1) # Glockenspiel
    player.set_instrument(11, 2) # Music Box
    player.set_instrument(12, 3) # Vibraphone

    scale_dict = {'Default': [100, 102, 107, 109], 'Major': [100, 104, 107, 109],
                  'Major 7': [100, 104, 107, 111], 'Minor': [100, 103, 107, 110],
                  'Insen': [100, 101, 105, 110], 'Dim 7': [100, 103, 106, 109]}
    notes = scale_dict['Default']
    default_click = 1 # Mouse Button 1

    def __init__(self, master):

        self.master = master
        self._createGUI()
        self.master.protocol('WM_DELETE_WINDOW', self._safe_close)

    def _createGUI(self):

        self.master.title('Tetratonic Squares')
        self.master.resizable(False, False)

        # Menu Configuration
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        # File
        self.file = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.file, label='File')
        self.file.add_command(label='Reset', command=self.reset)
        self.file.add_command(label='Quit', command=self._safe_close)

        self.buttons = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.buttons, label='Buttons')
        self.buttons.add_radiobutton(label='Left Click', command=lambda: self.set_click(1))
        self.buttons.add_radiobutton(label='Right Click', command=lambda: self.set_click(3))
        self.buttons.add_radiobutton(label='Middle Click', command=lambda: self.set_click(2))

        # Instruments
        self.instrument_dict = OrderedDict()
        self.instrument_dict['Piano'] = ['Acoustic Grand Piano', 'Bright Acoustic Piano','Electric Grand Piano', 'Honky-tonk Piano', 'Electric Piano 1','Electric Piano 2', 'Harpsichord', 'Clavi',]
        self.instrument_dict['Chromatic Percussion'] = ['Celesta', 'Glockenspiel', 'Music Box', 'Vibraphone', 'Marimba', 'Xylophone', 'Tubular Bells', 'Dulcimer']
        self.instrument_dict['Organ'] = ['Drawbar Organ', 'Percussive Organ', 'Rock Organ', 'Church Organ', 'Reed Organ', 'Accordion', 'Harmonica', 'Tango Accordion']
        self.instrument_dict['Guitar'] = ['Acoustic Guitar (nylon)', 'Acoustic Guitar (steel)', 'Electric Guitar (jazz)', 'Electric Guitar (clean)', 'Electric Guitar (muted)', 'Overdriven Guitar', 'Distortion Guitar', 'Guitar Harmonics']
        self.instrument_dict['Bass'] = ['Acoustic Bass', 'Electric Bass (finger)', 'Electric Bass (pick)', 'Fretless Bass', 'Slap Bass 1', 'Slap Bass 2', 'Synth Bass 1', 'Synth Bass 2']
        self.instrument_dict['Strings'] = ['Violin', 'Viola', 'Cello', 'Contrabass', 'Tremolo Strings', 'Pizzicato Strings', 'Orchestral Harp', 'Timpani']
        self.instrument_dict['Ensemble'] = ['String Ensemble 1', 'String Ensemble 2', 'Synth Strings 1', 'Synth Strings 2', 'Choir Aahs', 'Choir Oohs', 'Synth Voice', 'Orchestra Hit']
        self.instrument_dict['Brass'] = ['Trumpet', 'Trombone', 'Tuba', 'Muted Trumpet', 'French Horn', 'Brass Section', 'Synth Brass 1', 'Synth Brass 2']
        self.instrument_dict['Reed'] = ['Soprano Sax', 'Alto Sax', 'Tenor Sax', 'Baritone Sax', 'Oboe', 'English Horn', 'Bassoon', 'Clarinet']
        self.instrument_dict['Pipe'] = ['Piccolo', 'Flute', 'Recorder', 'Pan Flute', 'Blown Bottle', 'Shakuhachi', 'Whistle', 'Ocarina']
        self.instrument_dict['Synth Lead'] = ['Lead 1 (square)', 'Lead 2 (sawtooth)', 'Lead 3 (calliope)', 'Lead 4 (chiff)', 'Lead 5 (charang)', 'Lead 6 (voice)', 'Lead 7 (fifths)', 'Lead 8 (bass + lead)']
        self.instrument_dict['Synth Pad'] = ['Pad 1 (new age)', 'Pad 2 (warm)', 'Pad 3 (polysynth)', 'Pad 4 (choir)', 'Pad 5 (bowed)', 'Pad 6 (metallic)', 'Pad 7 (halo)', 'Pad 8 (sweep)']
        self.instrument_dict['Synth Effects'] = ['FX 1 (rain)', 'FX 2 (soundtrack)', 'FX 3 (crystal)', 'FX 4 (atmosphere)', 'FX 5 (brightness)', 'FX 6 (goblins)', 'FX 7 (echoes)', 'FX 8 (sci-fi)']
        self.instrument_dict['World'] = ['Sitar', 'Banjo', 'Shamisen', 'Koto', 'Kalimba', 'Bag pipe', 'Fiddle', 'Shanai']
        self.instrument_dict['Percussion'] = ['Tinkle Bell', 'Agogo', 'Steel Drums', 'Woodblock', 'Taiko Drum', 'Melodic Tom', 'Synth Drum', 'Reverse Cymbal']
        self.instrument_dict['Sound Effects'] = ['Guitar Fret Noise', 'Breath Noise', 'Seashore', 'Bird Tweet', 'Telephone Ring', 'Helicopter', 'Applause', 'Gunshot']

        self.instruments = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.instruments, label='Instruments')

        for family, instrument_list in self.instrument_dict.items():
            menu = Menu(self.menubar)
            self.instruments.add_cascade(menu=menu, label=family)
            for instrument in instrument_list:
                menu.add_command(label=instrument,
                command=lambda f=family, i=instrument: self.select_instrument(f, i))

        # Scales
        self.scales = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.scales, label='Scales')
        for name, scale in self.scale_dict.items():
            self.scales.add_command(label=name, command= lambda s=scale: self.set_scale(s))
        self.scales.add_separator()
        self.second, self.third, self.fourth = (IntVar(), IntVar(), IntVar())
        self.scales.add_command(label='Define Custom Scale', command=self.custom_scale)

        # Effects
        self.effects = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.effects, label='Effects')
        self.repeat, self.repeat_delay = (BooleanVar(), IntVar())
        self.repeat_delay.set(1000) # Default to 1000 milliseconds
        self.effects.add_checkbutton(label='Repeat', variable=self.repeat)
        self.effects.add_separator()
        self.effects.add_command(label='Repeat Options', command=self.repeat_popup)

        # Help
        self.help = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.help, label='Help')
        self.help.add_command(label='LOL, no', command=lambda: None)

        # GUI
        self.frame_main = ttk.Frame(self.master)
        self.frame_main.pack(side=TOP)
        self.green = Frame(self.frame_main, width=400, height=400, background='#56B949')
        self.green.grid(row=0, column=0)
        self.red = Frame(self.frame_main, width=400, height=400, background='#EE4035')
        self.red.grid(row=0, column=1)
        self.blue = Frame(self.frame_main, width=400, height=400, background='#30499B')
        self.blue.grid(row=1, column=0)
        self.orange = Frame(self.frame_main, width=400, height=400, background='#F0A32F')
        self.orange.grid(row=1, column=1)

        # Key Bindings
        for mouse_button in ['<Button-1>', '<Button-2>', '<Button-3>']:
            self.green.bind(mouse_button, lambda event, i=0: self.play_note(event, note=i))
            self.red.bind(mouse_button, lambda event, i=1: self.play_note(event, note=i))
            self.blue.bind(mouse_button, lambda event, i=2: self.play_note(event, note=i))
            self.orange.bind(mouse_button, lambda event, i=3: self.play_note(event, note=i))

    def play_note(self, event, note):
        if note in [0, 1]:
            note_code = self.notes[note] - self.calc_note(event.y)
        if note in [2, 3]:
            note_code = self.notes[note] - 48 + self.calc_note(event.y)
        if note in [0, 2]:
            self.player.note_on(note_code, self.calc_velocity(event.x), event.num)
        if note in [1, 3]:
            self.player.note_on(note_code, self.calc_velocity_right(event.x), event.num)
        if self.repeat.get():
            self.after_id = self.master.after(self.repeat_delay.get(), lambda e=event, i=note: self.play_note(e, note=i))

    def calc_velocity(self, x_pos):
        return round(127 * (x_pos / 400))

    def calc_velocity_right(self, x_pos):
        return 127 - round(127 * (x_pos / 400))

    def calc_note(self, y_pos):
        return 12 * round(4 * (y_pos) / 400)

    def set_scale(self, scale):
        self.notes = scale

    def set_custom_scale(self):
        self.notes = [100, 100 + self.second.get(), 100 + self.third.get(), 100 + self.fourth.get()]

    def repeat_popup(self):
        popup = Toplevel(self.master, background='#82afdd', width=100, height=100, padx=10, pady=15)
        popup.title('Repeat Delay')
        Spinbox(popup, from_=1, to=10000, width=8, textvariable=self.repeat_delay).grid(row=0, column=0)
        Label(popup, text='Delay in milliseconds between repeats', pady=10, background='#82afdd').grid(row=1, column=0)

    def custom_scale(self):
        popup = Toplevel(self.master, background='#83DE84', width=100, height=100, padx=10, pady=15)
        popup.title('Define Custom Scale')
        Spinbox(popup, values=('Root'), width=7).grid(row=0, column=0)
        Spinbox(popup, from_=0, to=11, width=7, textvariable=self.second, command=self.set_custom_scale).grid(row=0, column=1)
        Spinbox(popup, from_=0, to=11, width=7, textvariable=self.third, command=self.set_custom_scale).grid(row=0, column=2)
        Spinbox(popup, from_=0, to=11, width=7, textvariable=self.fourth, command=self.set_custom_scale).grid(row=0, column=3)
        Label(popup, text='Notes are measured in half steps above the Root', pady=10, background='#83DE84').grid(row=1, column=0, columnspan=4)

    def select_instrument(self, family, instrument):
        midi_code = ((list(self.instrument_dict.keys())).index(family) * 8
                    + self.instrument_dict[family].index(instrument))
        self.player.set_instrument(midi_code, self.default_click)

    def set_click(self, button):
        self.default_click = button

    def reset(self):
        self.master.after_cancel(self.after_id) # Isn't working for multiple afters?
        self.player.close()
        self.notes = [100, 102, 107, 109]
        self.repeat.set(False)
        self.repeat_delay.set(1000)
        self.player = midi.Output(0)
        self.player.set_instrument(10, 1)
        self.player.set_instrument(11, 2)
        self.player.set_instrument(12, 3)

    def _safe_close(self):
        self.player.close()
        self.master.destroy()

def main():

    root = Tk()
    app = tetratonicsquares(root)
    root.mainloop()

if __name__ == '__main__': main()
