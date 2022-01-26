#include<stdio.h>
#include<math.h>

int main(){

	int Nlmb=11;		// Number of grids/wave length
	float Crnt=0.975;	//Courant number
	float cT=3.0;		// T-wave velocity
	float cL=6.0;		// L-wave velocity

	float fin=5.0;		// central frequency

	printf("Nlmb ? (number of grids/wave length)\n");
	scanf("%d",&Nlmb);
	printf("fin  ? (source frequency )\n");
	scanf("%f",&fin);

	float T0=1.0/fin;	// fundamental period
	float lmbT=cT*T0;	// T-wave length
	float lmbL=cL*T0;	// L-wave length

	float dx_max=lmbT/Nlmb; // maximum grid spacing
	float dt_max=Crnt*dx_max/(sqrt(2.0)*cL); //maximum time increment


	printf(" Nlmb=%d,  Crnt=%lf \n",Nlmb,Crnt);
	printf(" cL=%lf, cT=%lf \n",cL,cT);
	printf(" frequency=%lf \n",fin);
	printf(" ---------------------------\n");
	printf(" dx=%lf  (1/dx=%lf)\n",dx_max,1.0/dx_max);
	printf(" dt=%lf  (1/dt=%lf)\n",dt_max,1.0/dt_max);

	return(0);
}
