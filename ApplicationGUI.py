import tkinter as tk
from tkinter import filedialog, Text, ttk, dialog
import os
from AudioController import AudioController
from AutomaticEq import AutomaticEq
import test_external_file as ext_file
import numpy as np
from Globals import *


class ApplicationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automatic Linearity Correction System - AutomaticEQ")

        self.__set_up_frames__()
        self.__set_up_buttons__()
        self.automatic_eq = AutomaticEq(target_level=0, reference_amplitude=0.05, narrow_bands=False)

    def __set_up_frames__(self):
        self.canvas = tk.Canvas(master=self.root, height=850, width=530, bg=GUI_COLOR_1)
        self.canvas.pack()  # .place(relwidth=1, relheight=1, relx=0, rely=0)

        self.text_frame = tk.Frame(master=self.root, bg=GUI_COLOR_1)
        self.text_frame.place(relwidth=0.8, relheight=0.78, relx=0.1, rely=0.01)

        self.buttons = tk.Frame(master=self.root, bg=GUI_COLOR_2)
        self.buttons.place(relwidth=0.8, relheight=0.15, relx=0.1, rely=0.8)

    def __set_up_buttons__(self):
        # Button definitions
        apply_eq = tk.Button(master=self.buttons,
                             bg=GUI_COLOR_2,
                             activebackground=GUI_COLOR_3,
                             activeforeground=GUI_COLOR_5,
                             fg=GUI_COLOR_6,
                             width=60,
                             text="Apply EQ to wave-file",
                             command=self.equalize_wave_file)
        learn = tk.Button(self.buttons,
                          bg=GUI_COLOR_2,
                          activebackground=GUI_COLOR_3,
                          activeforeground=GUI_COLOR_5,
                          fg=GUI_COLOR_6,
                          width=60,
                          text="Start learning",
                          command=self.start_learning)
        frequency_response = tk.Button(self.buttons,
                                       bg=GUI_COLOR_2,
                                       activebackground=GUI_COLOR_3,
                                       activeforeground=GUI_COLOR_5,
                                       fg=GUI_COLOR_6,
                                       width=60,
                                       text="Show current frequency response",
                                       command=self.show_frequency_response)
        coefficients = tk.Button(self.buttons,
                                 bg=GUI_COLOR_2,
                                 activebackground=GUI_COLOR_3,
                                 activeforeground=GUI_COLOR_5,
                                 fg=GUI_COLOR_6,
                                 width=60,
                                 text="Print EQ coefficients",
                                 command=self.print_coefficients)
        audio_devices = tk.Button(self.buttons,
                                  bg=GUI_COLOR_2,
                                  activebackground=GUI_COLOR_3,
                                  activeforeground=GUI_COLOR_5,
                                  fg=GUI_COLOR_6,
                                  width=60,
                                  text="Get Available Audio Devices",
                                  command=self.print_audio_devices)

        # Packing buttons
        learn.pack()  # .place(relx=0.117, rely=0.2)
        frequency_response.pack()  # .place(relx=0.117, rely=0.35)
        coefficients.pack()  # .place(relx=0.117, rely=0.5)
        apply_eq.pack()  # .place(relx=0.117, rely=0.65)
        audio_devices.pack()  # .place(relx=0.117, rely=0.8)

    def __set_label__(self, text):
        label = tk.Label(master=self.text_frame,
                         bg=GUI_COLOR_1,
                         activebackground=GUI_COLOR_2,
                         activeforeground=GUI_COLOR_5,
                         fg=GUI_COLOR_6,
                         text=text)
        label.pack()

    def __erase_text_frame__(self):
        for widget in self.text_frame.winfo_children():
            widget.destroy()

    def start_learning(self):
        # TODO: iteration, parameters
        i = 2
        self.__erase_text_frame__()
        self.automatic_eq.learn(iteration=i)
        self.__set_label__("Learning accomplished!")
        self.__set_label__("Performed " + str(i) + " iterations")

    def show_frequency_response(self):
        self.__erase_text_frame__()
        if hasattr(self.automatic_eq, "frequency_response"):
            self.__set_label__("Frequency response plot opened in a subview!")
            self.automatic_eq.plot_frequency_response()
        else:
            self.__set_label__("No learning has been conducted yet!")

    def print_coefficients(self):
        self.__erase_text_frame__()
        if not hasattr(self.automatic_eq, "coefficients"):
            self.__set_label__("No learning has been performed!")
            return
        self.__set_label__(" ")
        self.__set_label__("Used parameters:")
        self.__set_label__("Target level (dB): " + str(self.automatic_eq.target_level))
        self.__set_label__(
            "Reference amplitude (in a unified range: -1:1): " + str(self.automatic_eq.reference_amplitude))
        self.__set_label__("EQ frequencies: " + str(self.automatic_eq.center_frequencies))
        self.__set_label__("EQ Bandwidth: " + str(self.automatic_eq.bandwidth) + " octave")
        self.__set_label__(" ")
        self.__set_label__("Current EQ coefficients (after learning):")
        for x in self.automatic_eq.coefficients:
            db = str(x[1]) if x[1] < 0 else "+" + str(x[1])
            text = db + " dB at " + str(x[0]) + " Hz"
            self.__set_label__(text)

    def equalize_wave_file(self):
        self.__erase_text_frame__()
        if not hasattr(self.automatic_eq, "coefficients"):
            self.__set_label__("No learning performed!")
            return
        filename = filedialog.askopenfilename(initialdir="/", title="",
                                              filetypes=(("Wave files", "*.wav"), ("All files", "*.*")))
        self.__set_label__("Opened up: " + filename)
        wave, fs = ext_file.load_wave(filepath=filename, reference_amplitude=self.automatic_eq.reference_amplitude)
        left_channel, right_channel = zip(*wave)
        left_eq = self.automatic_eq.eq(data=left_channel, apply_only_bandpass=False)
        right_eq = self.automatic_eq.eq(data=right_channel, apply_only_bandpass=False)
        wave_eq = np.array(list(zip(left_eq, right_eq)))
        self.__set_label__("Wave file equalized according to established coefficients. Now playing:")
        AudioController.play_wave(wave_eq)

    def print_audio_devices(self):
        self.__erase_text_frame__()
        devices = AudioController.get_audio_devices()
        i = 0
        self.__set_label__("To use custom settings, please modify Globals.py")
        for device in devices:
            text = str(i) + ": " + \
                   str(device["name"]) + " i:" + \
                   str(device["max_input_channels"]) + " o:" + \
                   str(device["max_output_channels"])
            self.__set_label__(text)
            i += 1

    def run(self):
        self.root.mainloop()
