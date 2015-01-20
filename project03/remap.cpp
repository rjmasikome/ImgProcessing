#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <cmath>

 using namespace cv;

 /// Global variables
 Mat src, dst;
 Mat map_x, map_y;
 char* remap_window = "Remap demo";
 int ind = 0;

 /// Function Headers
 void update_map( void );

 /**
 * @function main
 */
 int main( int argc, char** argv )
 {
   /// Load the image
   src = imread( "bauckhage.jpg", 1 );

  /// Create dst, map_x and map_y with the same size as src:
  dst.create( src.size(), src.type() );
  map_x.create( src.size(), CV_32FC1 );
  map_y.create( src.size(), CV_32FC1 );

  /// Create window
  namedWindow( remap_window, CV_WINDOW_AUTOSIZE );

    /// Update map_x & map_y. Then apply remap
    update_map();
    
    remap( src, dst, map_x, map_y, CV_INTER_LINEAR, BORDER_CONSTANT, Scalar(0,0, 0) );
    /// Display results
    imshow( remap_window, dst );


    waitKey(0);
    double min, max;
    cv::minMaxLoc(map_y, &min, &max);
    std::cout<<min<<std::endl;
    std::cout<<max;
  return 0;
 }

 /**
 * @function update_map
 * @brief Fill the map_x and map_y matrices with 4 types of mappings
 */
 void update_map( void )
 {
    const float hRows = src.rows/2;
    const float hCols = src.cols/2;
    float angle, r;

   for( int y = 0; y < src.rows; y++ )
   { for( int x = 0; x < src.cols; x++ )
       {
        float newX = (x - hRows);
        float newY = (y - hCols);
        
        angle=atan2(newY, newX);
        if (angle < 0) {angle = angle+2*M_PI;}
        angle = angle *180/M_PI;
        angle = fmod((angle+180),360);
        angle = angle*256/360;

        r=sqrt(pow(newX,2)+pow(newY,2));
        
        map_x.at<float>(y,x) = angle;
        map_y.at<float>(y,x) = 2*(hRows-r);
        
       }
     }

    
}