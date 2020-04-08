
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
