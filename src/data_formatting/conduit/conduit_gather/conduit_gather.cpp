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
#include "conduit/conduit_relay_mpi.hpp"

using namespace conduit;
using namespace conduit::relay;

void process_arguments(int argc, char **argv,
                       int & numFiles,
                       char **& my_files) 
{
   // Get the number of processes
   int world_size;
   MPI_Comm_size(MPI_COMM_WORLD, &world_size);

   // Get the rank of the process
   int world_rank;
   MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

   int total_num_files = argc -1;
   int num_per_rank = total_num_files / world_size; 

   // determine total owned by my
   int num_owned_by_me = total_num_files / world_size;
   if (total_num_files % world_size > world_rank) {
      ++num_owned_by_me;
   }
   numFiles = num_owned_by_me;
   
   // determine starting index for number than I own
   int first_index = 0; 
   first_index += num_per_rank*world_rank;
   first_index += std::min(world_rank,total_num_files % world_size);
   my_files = &argv[1+first_index];

}

int printNode(Node & node) {
   node.info().print();
   node.schema().print();
   NodeIterator itr = node.children();

   while (itr.has_next()) {
      Node & n = itr.next();
      std::string n_name = itr.name();
      std::cout << n_name << std::endl;
   }
}


int main(int argc, char ** argv) {
   MPI_Init(&argc, &argv);

   // Get the rank of the process
   int world_rank;
   MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

   
   // Process command line
   int numFiles;
   char ** my_files;
   process_arguments(argc,argv,numFiles,my_files);

   Node n_load;
   for(int i = 0; i < numFiles; ++i) {
      char * fname = my_files[i];
      io::load(fname,"hdf5",n_load);
   }
   Node n_gather; 
   
   mpi::gather_using_schema(n_load,n_gather, 0, MPI_COMM_WORLD);


    if (world_rank == 0)
   {
      n_gather.print();
      Node n_save;
      NodeIterator itr = n_gather.children();
      std::ostringstream oss;
      int i =0; 
      while(itr.has_next())
      {
          Node &n_child = itr.next();
          oss.str("");
          oss << "rank_" << i;
          n_save[oss.str()].set_external(n_child);
          ++i;
      }
      io::save(n_save, "results.hdf5");
   }

   MPI_Finalize();
}
