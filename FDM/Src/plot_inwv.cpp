#include<stdio.h>
#include"fdm2d.h"


int main(){
	char fname[128];
	sprintf(fname,"%s","inwv0.dat");
	InWv iwv(fname);
	char fnout[128]="wvfm.dat";
	iwv.out(fnout);
};
