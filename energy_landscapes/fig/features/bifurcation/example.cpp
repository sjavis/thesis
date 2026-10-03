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


vector<vector<double>> path;
void trackPath(int iter, State& state) {
  auto coords = state.coords();
  if (iter==0 && path.empty()) path = {coords};
  if (vec::norm(coords - path.back()) > 0.05) path.push_back(coords);
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
  Potential pot(pathwayEG);
  State state1(pot, {-1,0});
  State state2(pot, {1,-1});
  State state3(pot, {1,1});
  auto min1 = min.minimise(state1);
  auto min2 = min.minimise(state2);
  auto min3 = min.minimise(state3);
  saveFile("minima.txt", {min1, min2, min3});

  // Get TS
  Bitss bitss1(state1, state2);
  Bitss bitss2(state2, state3);
  auto ts1 = bitss1.run();
  auto ts2 = bitss2.run();
  saveFile("transitions.txt", {ts1, ts2});

  // Path from top TS
  Downhill downhill(bitss1.getPair(), 0.05);
  auto path = downhill.run();
  // GradDescent gd;
  // State tsSide1(pot, ts1 + vector<double>{-0.001, 0.01});
  // State tsSide2(pot, ts1 + vector<double>{ 0.001, 0.01});
  // path.clear();
  // gd.minimise(tsSide1, trackPath);
  // std::reverse(path.begin(), path.end());
  // gd.minimise(tsSide2, trackPath);
  saveFile("path.txt", path);

  return 0;
}
