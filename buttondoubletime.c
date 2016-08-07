#include <wiringPi.h>
#include <stdio.h>


#define   SDI   0   //serial data input
#define   RCLK  1   //memory clock input(STCP)
#define   SRCLK 2   //shift register clock input(SHCP)

#define SDIB 3
#define RCLKB 4
#define SRCLKB 5
#define BTN 6

/*
#define SDI 11
#define RCLK 12
#define SRCLK 13
#define SDIB 15
#define RCLKB 16
#define SRCLKB 18
#define BTN 22
/*
/*

SDI   = 11
RCLK  = 12
SRCLK = 13
SDIB = 15
RCLKB = 16
SRCLKB = 18
BTN = 22
*/

unsigned char SegCode[17] = {0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71,0x80};
unsigned char codeDash = 0x40;
/*
#code0=0x3f
#code1=0x06
#code2=0x5b
#code3=0x4f
#code4=0x66
#code5=0x6d
#code6=0x7d
#code7=0x07
#code8=0x7f
#code9=0x6f
#codeA=0x77
#codeB=0x7c
#codeC=0x39
#codeD=0x5e
#codeE=0x79
#codeF=0x71
codeDash=0x40
#codeDot=0x80
*/

void init(void)
{
        pinMode(SDI, OUTPUT); //make P0 output
        pinMode(RCLK, OUTPUT); //make P0 output
        pinMode(SRCLK, OUTPUT); //make P0 output
        pinMode(SDIB, OUTPUT); //make P0 output
        pinMode(RCLKB, OUTPUT); //make P0 output
        pinMode(SRCLKB, OUTPUT); //make P0 output

        digitalWrite(SDI, 0);
        digitalWrite(RCLK, 0);
        digitalWrite(SRCLK, 0);
        digitalWrite(SDIB, 0);
        digitalWrite(RCLKB, 0);
        digitalWrite(SRCLKB, 0);        
}

void hc595_shift(unsigned char dat)
{
        int i;

        for(i=0;i<8;i++){
                digitalWrite(SDI, 0x80 & (dat << i));
                digitalWrite(SRCLK, 1);
                digitalWrite(SDIB, 0x80 & (dat << i));
                digitalWrite(SRCLKB, 1);
                                delay(1);
                digitalWrite(SRCLK, 0);
                digitalWrite(SRCLKB, 0);                
        }

                digitalWrite(RCLK, 1);
                digitalWrite(RCLKB, 1);
                delay(1);
                digitalWrite(RCLK, 0);
                digitalWrite(RCLKB, 0);
}

int main(void)
{
        int i;

        if(wiringPiSetup() == -1){ //when initialize wiring failed,print messageto screen
                printf("setup wiringPi failed !");
                return 1;
        }

        init();

        while(1){
                for(i=0;i<17;i++){
                        hc595_shift(SegCode[i]);
                        delay(500);
                }
        }

        return 0;
}


