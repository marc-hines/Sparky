#include "main.h"
#include "global.h"

Globalstruct global;

char *Logon = "ADP";
char *Filename = "DICT PRIVLIB";
//char *Itemname = "7YR_BACKUP-FLAG";
char *Itemname = "DNA";
int err;

char *getenv();

static RFC_FILE dict_fh;
static RLC_LIST dict_lh;

#define DICT_BUF_SIZE 10000
static char dict_data[DICT_BUF_SIZE];
static int item_len;

int main (int argc, char *argv[])
{
char marc[100];
strcpy(marc,"test");
global.MoreStuff = marc;

   if ((global.Database = getenv("REALDBASE")) == NULL)
   {
      fprintf(stderr,"Fatal error! Environment: $REALDBASE not set\n");
      exit(1);
   }

   fprintf(stderr,"Environment: $REALDBASE is %s\n",global.Database);

   if (err = RfcConnect(global.Database, NULL, NULL, Logon, NULL))
   {
       fprintf(stderr,"RfcConnect: %s\n",RgcErrMsg(err));
       exit(1);
   }

   if (err = RfcOpenFile(Filename,&dict_fh)) {
       fprintf(stderr,"Cannot open file: %s\n",Filename);
       exit(1);
    }

   int id_len;
 
   id_len = strlen(Itemname);
   if (err = RfcRead(dict_fh, Itemname, id_len, dict_data, DICT_BUF_SIZE, &item_len)) {
      fprintf(stderr,"%s %s not found",Filename, Itemname);
   }
   dict_data[item_len] = '\0';

   printf("%s %s: %s\n",Filename, Itemname, dict_data);

   exit(0);

}
