#include <cerrno>
#include <fstream>
#include <iostream>
#include <string> 

#include "conduit/conduit.hpp"
#include "conduit/conduit_relay.hpp"


using namespace conduit;
using namespace conduit::relay;


/* from http://insanecoding.blogspot.com/2011/11/how-to-read-in-file-in-c.html */
std::string get_file_contents(const char *filename)
{
  std::ifstream in(filename, std::ios::in | std::ios::binary);
  if (in)
  {
    std::string contents;
    in.seekg(0, std::ios::end);
    contents.resize(in.tellg());
    in.seekg(0, std::ios::beg);
    in.read(&contents[0], contents.size());
    in.close();
    return(contents);
  }
  throw(errno);
}

int main(int argc, char *argv[]){
   int numfiles = argc - 3;
   char ** fnames = &argv[3];
   char * outname = argv[2];
   char * schema_file = argv[1];
   std::string schema = get_file_contents(schema_file);

   Generator g(schema,"json");
   Node schema_node;
   g.walk_external(schema_node);

   Node tree;

   for (int i = 0; i < numfiles; ++i ) {
      Node unfiltered_file;
      io::load(fnames[i],"hdf5",unfiltered_file);
      Node & filtered_file = tree[std::to_string(i)];
      /* copy the schame into the node for filtered_file */
      filtered_file = schema_node;
      /* update any compatible entries from the file */
      filtered_file.update_compatible(unfiltered_file);
   }

   io::save(tree, outname,"hdf5");

}
