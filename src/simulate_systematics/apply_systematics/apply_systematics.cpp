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

const gsl_rng_type *Gen_Type; //Type of random number generator to use.
gsl_rng *Gen; //The actual generator object.
vector<string> read_mask(string filename){
  cout << "Reading mask from: " << filename.c_str() << endl;
  ifstream ifile(filename.c_str());
  if( !ifile){
    cout << "ERROR: Error opening "<< filename <<"." << endl;
    exit (EXIT_FAILURE);
  }
  string line;
  vector<string> mask;
  while(getline(ifile, line)){
    istringstream iline(line);
    mask.push_back(line);
  } 
  cout << "Read mask from: " << filename.c_str() << endl;
  ifile.close();
  return mask;
}


int main(int argc, char const *argv[]){
  if (argc != 7){
    cout << "ERROR: Unexpected number of arguments." << endl;
    cout << "USAGE: " << argv[0] << " CATALOG SEED OUTPUT_BASE SAVE_VETO SAVE_ANG SAVE_ALL" << endl;
    return 1;
  } 
  int  seed = atoi(argv[2]);
  string catalog_filename = argv[1];
  bool save_veto=atoi(argv[4]);
  bool save_ang=atoi(argv[5]);
  bool save_all=atoi(argv[6]);
  gsl_rng_env_setup(); //Setup environment variables.
  Gen_Type = gsl_rng_taus; //The fastest random number generator.
  Gen = gsl_rng_alloc(Gen_Type); //Allocate necessary memory, initialize generator object.
  gsl_rng_set(Gen, seed); //Seed the generator

  vector<string> vetomask = read_mask("../vetomask_s42_nbar3.9770e-04.dat");
  vector<string> angmask = read_mask("../angmask_s2_nbar3.9770e-04.dat");
  ifstream catalog(catalog_filename.c_str());
  if( !catalog){
    cout << "ERROR: Error opening file." << endl;
    exit (EXIT_FAILURE);
  }
  double x, y, z, r;
  string line;
  double x1, x2, y1, y2;
  while(getline(catalog, line)){
    istringstream iline(line);
    iline >> x >> y >> z >> r;
    bool vetoflag=0;
    for(int i=0; i<vetomask.size(); i++){
      istringstream maskline(vetomask[i]);
      maskline >> x1 >> x2 >> y1 >> y2;
      if(x > x1 && x < x2 && y > y1 && y < y2 && !vetoflag){
        vetoflag=1;
        break;
      }
    }
    double completeness;
    double completeness_tot=1;
    bool compflag=0;
    for(int i=0; i<angmask.size(); i++){
      istringstream maskline(angmask[i]);
      maskline >> x1 >> x2 >> y1 >> y2 >> completeness;
      if(x > x1 && x < x2 && y > y1 && y < y2){
        cout << completeness<<endl;
        completeness_tot*=completeness;
      }
    }
    if ( completeness_tot < 1 ){
        if ( (gsl_rng_uniform(Gen) < completeness_tot) ){
            cout << x << ' ' << y << ' ' << z << ' ' << r << endl;
        }
    }
    else{ cout << x << ' ' << y << ' ' << z << ' ' << r << endl;}
    cout << completeness_tot <<endl;
    //break;
  }
  catalog.close();

  gsl_rng_free(Gen);
  return 0;
}

