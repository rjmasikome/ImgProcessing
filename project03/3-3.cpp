#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <cmath>

using namespace cv;
using namespace std;

int HoleRadius, leanX, leanY;
Mat image, output, IndexX, IndexY;
string ImageName;
string anamorphosis = "Disk and ellipse anamorphosis";

void MapIndex( void );

static void InputImage()
{ 
  while (true)
  {
    cout << "\tPlease enter image name:\n\t";
    cin >> ImageName;
    image = imread( ImageName, 1 );
      if(!image.empty())
      {
        break;
      }
      else
      {
        cout << "\tImage does not exist. Try other name or put the file extension\n\n\n";
      }
  }
}

static void InputParameter()
{
  
  while (true)
  {
    cout << "\n\n\tPlease enter radius (Integer) of the hole \n\t(Enter 0 for default):\n\t";
    cin >> HoleRadius;
      if(cin.good()){
          break;
      }
      else{
          cout << "Error. The value is not integer." << std::endl;
          cin.clear();
          cin.ignore(INT_MAX, '\n');
      }
  }
  while (true)
  {
    cout << "\n\n\tPlease enter the stretch value (Integer) to X axis \n\t(Enter 0 for default):\n\t";
    cin >> leanX;
      if(cin.good()){
          break;
      }
      else{
          cout << "Error. The value is not integer." << std::endl;
          cin.clear();
          cin.ignore(INT_MAX, '\n');
      }
  }
  while (true)
  {
    cout << "\n\n\tPlease enter the stretch value (Integer) to Y axis \n\t(Enter 0 for default):\n\t";
    cin >> leanY;
      if(cin.good()){
          break;
      }
      else{
          cout << "Error. The value is not integer." << std::endl;
          cin.clear();
          cin.ignore(INT_MAX, '\n');
      }
  }
}

int main( int argc, char** argv )
{
  cout << "Disk and ellipse anamorphosis"
      "\nFor Image Processing Project 3-3\n\n";

  InputImage();  

  // Commented snippet below is for debugging
  // image = imread( "asterixGrey.jpg", 1 );
  // image = imread( "bauckhage.jpg", 1 );

  output.create( image.rows,image.rows, image.type() );
  IndexX.create( image.rows,image.rows, CV_32FC1 );
  IndexY.create( image.rows,image.rows, CV_32FC1 );

  InputParameter();

  MapIndex();
    
  remap( image, output, IndexX, IndexY, CV_INTER_LINEAR, BORDER_CONSTANT, Scalar(0,0, 0) );
  namedWindow( anamorphosis, CV_WINDOW_AUTOSIZE );

  imwrite( "3-3.jpg", output);

  imshow( anamorphosis, output );

  waitKey(0);
  return 0;
}

void MapIndex( void )
{
  const float hRows = image.rows/2;
  float angle, r;

  for( int y = 0; y < image.rows; y++ )
  { for( int x = 0; x < image.rows; x++ )
    {
      float newX = (x - hRows);
      float newY = (y - hRows);
      
      angle=atan2(newY, newX);
      if (angle < 0) {angle = angle+2*M_PI;}
      angle = angle *180/M_PI;
      angle = fmod((angle+180),360);
      angle = angle*(image.cols-2)/360;

      r=sqrt(pow(newX,2)/((10+leanX)/10)+pow(newY,2)/((10+leanY)/10));
      
      IndexX.at<float>(y,x) = angle;
      IndexY.at<float>(y,x) = 2*(hRows-r)+HoleRadius;
      
    }
  }  
}