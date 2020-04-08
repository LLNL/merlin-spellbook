////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2019, Lawrence Livermore National Security, LLC.
// Produced at the Lawrence Livermore National Laboratory
// Written by the Merlin dev team, listed in the CONTRIBUTORS file.
// <merlin@llnl.gov>
//
// LLNL-CODE-797170
// All rights reserved.
// This file is part of merlin-spellbook.
//
// For details, see https://github.com/LLNL/merlin-spellbook and
// https://github.com/LLNL/merlin.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
////////////////////////////////////////////////////////////////////////////////


#include "conduit/conduit.hpp"
#include "conduit/conduit_relay.hpp"

using namespace conduit;
using namespace conduit::relay;

int main(int argc, char ** argv) {

   char * fname = argv[1];

   Node n_load;
   io::load(fname,"hdf5",n_load);
   n_load.info().print();
   n_load.schema().print();
   n_load["0/outputs/images/0"].print();
   double * abs_image = n_load["0/outputs/images/0/abs"].value();

   NodeIterator itr = n_load["0/outputs/images"].children();

   while (itr.has_next()) {
      Node & n = itr.next();
      std::string n_name = itr.name();
      std::cout << n_name << std::endl;
   }
}
