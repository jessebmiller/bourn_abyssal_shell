# Bourn Abyssal SHell

A toy linux shell mystery cosmic horror game and an experiment with AI.

## Design goals

It should feel like you are poking around in a linux system. It should
feel familiar if you know the linux terminal. If not you should be
able to learn a little linux terminal by messing around. There should
also be a coherant mystery (or a few, different ones each time) that
you can uncover.

* Simplicity. The interface is just a prompt and responses.
* Fun. It's more important for it to be fun to poke around in this
  system and uncover the mysteries than for it to be a reliable linux
  interface
* Coherent mysteries, no matter what order the mysteries are
  uncovered, the more coherant and narrative the throughline the
  better
* reliable linux interface. Commands do what they're supposed
  to. Files you write stick around. Programs don't work unless you
  install them. It should feel like a real linux install.

## Architecture and stack

HTMX frontend with prompt input field and scrolling text output window.

Python server that takes the user input, wraps it in a prompt for GPT
(or another LLM), perhaps doing a few round trips with more prompts to
the LLM (if that's adorable) then sends down html to add to the
scrolling text output window.

Server caches the requests and responses per session so it can send a
history of the conversation to the LLM as needed

No build system if we can get away with it

# in repo kanban board

This repo uses a git committed kanban board. Install
[hammock](https://github.com/jessebmiller/hammock) to use it. It's
really only built for my personal use, but if you want to use it, I'll
try and make it work for you. The docs over there are pretty out of
date too. /shrug
