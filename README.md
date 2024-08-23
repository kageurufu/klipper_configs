# Frank's Klipper Configurations

I'm trying to organize my configurations, and abusing git to do it.

Different parts of my configurations will be stored in separate orphaned git branches, and globally shared configurations will be in their own branches

## Global configuration

* [`board-definitions`](./board_definitions/) 
  
  `[board_pin]`s and custom thermistor definitions as needed 

* [`global-config`](./global_config/)

  Shared macros and configuration blocks needed by all my printers


## Printers

* [Ganymede](./printer/ganymede) - Voron V2.4, my workhorse
* [Leda](./printer/leda/) - Voron V0.2 (mostly)

### My Other Printers

* Voron Phoenix - In-progress build
* RatRig V-Minion - In-progress build
* DoomFork - In repair
* Peopoly Magneto X - In repair
* Amalthea - Elegoo Jupiter, not klipper