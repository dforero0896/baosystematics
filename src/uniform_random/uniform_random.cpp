/*
g++ -fopenmp -o uniform_random.o uniform_random.cpp `gsl-config --cflags --libs`
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

const gsl_rng_type *Gen_Type; //Type of random number generator to use.
gsl_rng *Gen; //The actual generator object.
const int TIMES = 10;

int main(int argc, char const *argv[]){
  if (argc != 4){
    cout << "ERROR: Unexpected number of arguments." << endl;
    cout << "USAGE: " << argv[0] << " N_OBJECTS SEED OUTPUT" << endl;
    return 1;
  } 
  int n_objects = atoi(argv[1]);
  unsigned long int seed = atoi(argv[2]);
  string outpath = argv[3];
  int n_random_objects = TIMES * n_objects;
  gsl_rng_env_setup(); //Setup environment variables.
  Gen_Type = gsl_rng_taus; //The fastest random number generator.
  Gen = gsl_rng_alloc(Gen_Type); //Allocate necessary memory, initialize generator object.
  gsl_rng_set(Gen, seed); //Seed the generator
  ofstream ofile;
  ofile.open(outpath.c_str());
  for (int i = 0 ; i<n_random_objects; i++){ 
    for (int k=0 ; k < 3 ; k++){
      double random = 2500 * gsl_rng_uniform(Gen);
      ofile << random << " ";
    }
    ofile << "\b" << endl;
  }

  ofile.close();


  gsl_rng_free(Gen);
  return 0;
}

