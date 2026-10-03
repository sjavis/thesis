#include "ellib.h"
#include <fstream>
#include <string>

using namespace ellib;
using std::vector;


vector<vector<double>> peaks;

void readPeaks() {
  std::ifstream file("peaks.txt");
  file.ignore(99999, '\n');
  while (!file.eof()) {
    vector<double> peak(5);
    file >> peak[0] >> peak[1] >> peak[2] >> peak[3] >> peak[4];
    if (file.eof()) break;
    peaks.push_back(peak);
  }
  file.close();
}


void saveFile(std::string filename, vector<vector<double>> states) {
  std::ofstream file(filename);
  for (auto coords: states) {
    for (double x: coords) {
      file << " " << x;
    }
    file << std::endl;
  }
  file.close();
}


void pathwayEG(const vector<double>& coords, double* e, vector<double>* g) {
  if (e) *e = 0;
  if (g) *g = vector<double>(2);
  for (auto peak: peaks) {
    double dx = (coords[0] - peak[1]) / peak[3];
    double dy = (coords[1] - peak[2]) / peak[4];
    double epeak = peak[0] * exp(- dx*dx - dy*dy);
    if (e) *e += epeak;
    if (g) *g -= vector<double>{2*dx/peak[3], 2*dy/peak[4]} * epeak;
   }
}


int main(int argc, char** argv) {
  mpiInit(&argc, &argv);
  print();
  readPeaks();

  // Get minima
  Lbfgs min;
  auto state1 = State(Potential(pathwayEG), {-1,0});
  auto state2 = State(Potential(pathwayEG), {1,0});
  auto min1 = min.minimise(state1);
  auto min2 = min.minimise(state2);
  saveFile("minima.txt", {min1, min2});

  // Get TS
  Bitss bitss(state1, state2);
  auto ts = bitss.run();
  saveFile("transitions.txt", {ts});

  // Path
  Neb neb(Potential(pathwayEG), min1, min2, 20);
  neb.setHybrid(1, 100);
  auto chain = neb.run();
  saveFile("path.txt", chain);

  return 0;
}
