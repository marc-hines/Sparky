#include <rgc.h>
#include <rfc.h>
#include <rlc.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLD_SEP	"\375"	  /* literal equiv of MV_FLAG */
#define AT_FLAG	0xFE			/* multivalue flag for workfiles */
#define MV_FLAG	0xFD			/* multivalue flag for workfiles */
#define SV_FLAG	0xFC			/* multivalue flag for workfiles */

#define FATAL 1
#define NON_FATAL 0
