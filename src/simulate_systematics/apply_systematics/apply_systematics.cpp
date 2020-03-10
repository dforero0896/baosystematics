/*
g++ -fopenmp -o apply_systematics apply_systematics.cpp `gsl-config --cflags --libs`
 */
#include <iostream>
using namespace std;
#include <sstream>
#include <string>
#include <fstream>
#include <time.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <sys/time.h>
#include <vector>
#include<cmath>
#include <unistd.h>

const gsl_rng_type *Gen_Type; //Type of random number generator to use.
gsl_rng *Gen; //The actual generator object.

vector< vector<double> > read_mask(string filename){
  /* Reads a mask file into a vector */
  cout << "==> Reading mask from: " << filename.c_str() << endl;
  ifstream ifile(filename.c_str());
  if( !ifile){
    cout << "ERROR: Error opening "<< filename <<"." << endl;
    exit (EXIT_FAILURE);
  }
  string line;
  vector<vector<double> > mask;
  double buffer;
  /* Read rows */
  while(getline(ifile, line)){
    istringstream iline(line);
    /* Read columns */
    vector<double> patch;
    while(iline >> buffer){
      patch.push_back(buffer);
    }
    mask.push_back(patch);
  } 
  cout << "==> Read mask from: " << filename.c_str() << endl;
  ifile.close();
  return mask;
}


int main(int argc, char const *argv[]){
  if (argc != 7 && argc != 8){
    cout << "ERROR: Unexpected number of arguments." << endl;
    cout << "USAGE: " << argv[0] << " CATALOG SEED OUTPUT_BASE VETO_MASK ANG_MASK SAVE [SUFFIX]" << endl;
    return 1;
  } 
  /* Read inputs*/
  int  seed = atoi(argv[2]);
  string catalog_filename = argv[1];
  string output = argv[3];
  string VETO_MASK_FN = argv[4];
  string ANG_MASK_FN = argv[5];
  int SAVE = atoi(argv[6]);
  string suffix;
  if( argc == 8 ){suffix = "."+string(argv[7]);}
  else {suffix = "";}
  /* Set up GSL random number generator */
  gsl_rng_env_setup(); //Setup environment variables.
  Gen_Type = gsl_rng_taus; //The fastest random number generator.
  Gen = gsl_rng_alloc(Gen_Type); //Allocate necessary memory, initialize generator object.
  gsl_rng_set(Gen, seed); //Seed the generator
  /* Read available masks */
  vector<vector<double> > vetomask = read_mask(VETO_MASK_FN);
  vector<vector<double> > angmask = read_mask(ANG_MASK_FN);
  /* Open catalog */
  ifstream catalog(catalog_filename.c_str());
  if( !catalog){
    cout << "ERROR: Error opening file." << endl;
    exit (EXIT_FAILURE);
  }
  double x, y, z, r; //Object coordinates
  string line;
  double x1, x2, y1, y2; // Patch corners
  /* Open output files */
  string  vetocat_fn = output+".VETO"+suffix+".dat";
  string  angcat_fn = output+".ANG"+suffix+".dat";
  string  vetoangcat_fn = output+".VETO_ANG"+suffix+".dat";
  ofstream vetocat, angcat, vetoangcat;
  if ( SAVE==1 || SAVE==4 ){
    vetocat.open(vetocat_fn.c_str());
  }
  if ( SAVE==2 || SAVE==4 ){
    angcat.open(angcat_fn.c_str());
  }
  if ( SAVE==3 || SAVE==4 ){
    vetoangcat.open(vetoangcat_fn.c_str());
  }
  if( !vetocat || !angcat || !vetoangcat ){
    cout << "ERROR: Error opening output files." << endl;
    exit (EXIT_FAILURE);
  }
  int testit=0;
  float veto_weight, ang_weight, vetoang_weight;
  double completeness;
  double completeness_tot;
  cout << "==> Masking file " << catalog_filename << endl;
  while(getline(catalog, line)){
    istringstream iline(line);
    iline >> x >> y >> z >> r;
    /* Check if object is masked by vetomask */
    veto_weight=1;
    for(int i=0; i<vetomask.size(); i++){
      x1 = vetomask[i][0];
      x2 = vetomask[i][1];
      y1 = vetomask[i][2];
      y2 = vetomask[i][3];
      if(x > x1 && x < x2 && y > y1 && y < y2){// If masked
        veto_weight=0;
        break; //Not necessary to check more patches
      }
    }
    /* Check if object is masked by angular mask */
    completeness_tot=1;
    for(int i=0; i<angmask.size(); i++){
      x1 = angmask[i][0];
      x2 = angmask[i][1];
      y1 = angmask[i][2];
      y2 = angmask[i][3];
      completeness = angmask[i][4];
      if(x > x1 && x < x2 && y > y1 && y < y2){//Update completeness
        completeness_tot*=completeness;
      }
      if(completeness_tot < 0.5){cout << completeness_tot<<endl;}
    }
    ang_weight = 1. / completeness_tot;
    if ( completeness_tot < 1 ){// If masked
      if ( (gsl_rng_uniform(Gen) > completeness_tot) || (completeness_tot < 0.5) ){//Prob. NOT to be saved.
        ang_weight = 0;
      }
    }
    vetoang_weight = veto_weight * ang_weight;
    if (veto_weight != 0 & (SAVE == 1 || SAVE == 4)){
      vetocat << x << '\t' << y << '\t' << z << '\t' << r << '\t' << veto_weight << endl;
    }
    if (ang_weight != 0 & (SAVE == 2 || SAVE == 4)){
      angcat << x << '\t' << y << '\t' << z << '\t' << r << '\t' << ang_weight << endl;
    }
    if (vetoang_weight != 0 & (SAVE == 3 || SAVE ==4)){
      vetoangcat << x << '\t' << y << '\t' << z << '\t' << r << '\t' << vetoang_weight << endl;
    }
    // To save only one catalog with multiple weight columns  
    //outcat << x << '\t' << y << '\t' << z << '\t' << r << '\t' << veto_weight << '\t' << ang_weight << '\t' << vetoang_weight << endl;
    testit++;
    //if(testit==1000){break;}
  }
  catalog.close();
  if ( SAVE==1 || SAVE==4 ){
    vetocat.close();
  }
  if ( SAVE==2 || SAVE==4 ){
    angcat.close();
  }
  if ( SAVE==3 || SAVE==4 ){
    vetoangcat.close();
  }
  //outcat.close();
  gsl_rng_free(Gen);
  return 0;
}

