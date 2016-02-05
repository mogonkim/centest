#include "cMatch.h"
#include <limits>

using namespace stereo;

// Census Radius and Width
#define		C_R		(3)
#define		C_W		(2*C_R+1)

// Box Filter Radius and Width
#define		B_R		(3)
#define		B_W		(2*B_R+1)

// y,x
const int samples[] =
{ 
	-3,-2,
    -3, 0,
    -3, 2,
	-2,-3,
    -2,-1,
    -2, 1,
    -2, 3,
	-1,-2,
    -1, 0,
    -1, 2,
	 0,-3,
     0,-1,
     0, 1,
     0, 3,
	 1,-2,
     1, 0,
     1, 2,
	 2,-3,
     2,-1,
     2, 1,
     2, 3,
	 3,-2,
     3, 0,
     3, 2
};


CensusMatch::CensusMatch(int w, int h, int d, int m)
	: StereoMatch(w, h, d, m), costs(w*d)
{

}

void CensusMatch::match(img::Img<uint8_t> & left, img::Img<uint8_t> & right, img::Img<uint16_t> & disp)
{
    costs.assign(width*maxdisp,std::numeric_limits<uint16_t>::max());
}
