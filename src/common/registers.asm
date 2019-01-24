REG_Joypad EQU $00

REG_Divider EQU $04

REG_Interrupt_Flag EQU $0F

REG_Sound1_Sweep EQU $10
REG_Sound1_LengthDuty EQU $11
REG_Sound1_VolumeEnvelope EQU $12
REG_Sound1_FreqLow EQU $13
REG_Sound1_FreqHi EQU $14

REG_Sound_MasterVolume EQU $24
REG_Sound_Panning EQU $25
REG_Sound_OnOff EQU $26

REG_LCD_Control EQU $40
REG_LCD_Status EQU $41

; BG scrolling
REG_Scroll_Y EQU $42
REG_Scroll_X EQU $43

REG_LCD_Y EQU $44
REG_LCD_Y_Compare EQU $45

REG_OAM_DMA EQU $46

; LCD Monochrome Palettes, Non-GBC-mode only
REG_BG_Palette EQU $47
REG_OB_Palette_1 EQU $48
REG_OB_Palette_2 EQU $49

REG_CGB_Speed_Switch EQU $4D

REG_CGB_VRAM_Bank EQU $4F

REG_CGB_BG_Palette_Index EQU $68
REG_CGB_BG_Palette_Data EQU $69
REG_CGB_Sprite_Palette_Index EQU $6A
REG_CGB_Sprite_Palette_Data EQU $6B

REG_CGB_WRAM_Bank EQU $70


HRAM_Leaf_Begin EQU $E0
HRAM_Leaf_End EQU $FE


REG_Interrupt_Enable EQU $FF
