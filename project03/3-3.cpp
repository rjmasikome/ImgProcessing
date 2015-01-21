//
//  3-3.cpp
//  ImageProcessingProject3
//
//  Created by Rian Josua Masikome on 1/19/15.
//  Copyright (c) 2015 Rian Josua Masikome. All rights reserved.
//
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <cmath>

using namespace cv;
using namespace std;

//
// Initializing the variables and function
// cv::Mat type for the image source and destination and also the output index
//
//
int HoleRadius, leanX, leanY;
Mat image, output, IndexX, IndexY;
string ImageName;
string anamorphosis = "Disk and ellipse anamorphosis";

void MapIndex( void );

//
//Function to get the image and also some error checking
//Jump to function main() to see how the program works
//
//
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

//
//Function to get the parameter for the image manipulation
//
//
static void InputParameter()
{
  
  //Get the radius of the hole in the image
  while (true)
  {
    cout << "\n\n\tPlease enter radius (Integer) of the hole \n\t(Enter 0 for default):\n\t";
    cin >> HoleRadius;
      if(cin.good()){
          break;
      }
      else{
          cout << "\tError. The value is not integer." << std::endl;
          cin.clear();
          cin.ignore(INT_MAX, '\n');
      }
  }

  //Get the parameter of ellipse on which axis the image will be leaning to
  //The following parameter if positive inserted will make the image lean towards X axis
  while (true)
  {
    cout << "\n\n\tPlease enter the stretch value (Integer) to X axis \n\t(Enter 0 for default):\n\t";
    cin >> leanX;
      if(cin.good()){
          break;
      }
      else{
          cout << "\tError. The value is not integer." << std::endl;
          cin.clear();
          cin.ignore(INT_MAX, '\n');
      }
  }


  //Get the parameter of ellipse on which axis the image will be leaning to
  //The following parameter if positive inserted will make the image lean towards Y axis
  while (true)
  {
    cout << "\n\n\tPlease enter the stretch value (Integer) to Y axis \n\t(Enter 0 for default):\n\t";
    cin >> leanY;
      if(cin.good()){
          break;
      }
      else{
          cout << "\tError. The value is not integer." << std::endl;
          cin.clear();
          cin.ignore(INT_MAX, '\n');
      }
  }
}

//
// The main function
//
//
int main( int argc, char** argv )
{
  cout << "Disk and ellipse anamorphosis"
      "\nFor Image Processing Project 3-3\n\n";

  //Get the image name from user
  InputImage();  

  // Commented snippet below is for debugging
  // image = imread( "asterixGrey.jpg", 1 );
  // image = imread( "bauckhage.jpg", 1 );

  //Create a matrix based on the input rows.
  //In this transformation, the image rows will be the sample for the radius of the new image
  output.create( image.rows,image.rows, image.type() );
  IndexX.create( image.rows,image.rows, CV_32FC1 );
  IndexY.create( image.rows,image.rows, CV_32FC1 );

  //Get the parameter from the user
  InputParameter();

  //This is where the magic happens.
  //The index referral of the new image is generated.
  MapIndex();
    
<<<<<<< HEAD
  //remap( image, output, IndexX, IndexY, CV_INTER_LINEAR, BORDER_CONSTANT, Scalar(0,0, 0) );
    
    for (int x=0; x<image.rows; x++) {
        const uchar* it = image.ptr<uchar>(x);
        uchar* it_dest = output.ptr<uchar>(x);
        for (int y=0; y<image.cols; y++)
        {
            IndexX.at<float>(y,x) = angle;
            IndexY.at<float>(y,x) = 2*(hRows-r)+HoleRadius;
            if (x_new < output.rows || x_new > 0) {
                if (y_new < output.cols || y_new > 0) {
                    it_dest[y+y_new+x_new*img_new.cols] = it[y];
                }
            }
        }
    }
    
=======
  //Map the new image based on the index generated from MapIndex() function
  //This function is inplace, where it will write to the second parameter which should be cv::Mat type
  remap( image, output, IndexX, IndexY, CV_INTER_LINEAR, BORDER_CONSTANT, Scalar(0,0, 0) );
  
  //Create the GUI window
>>>>>>> FETCH_HEAD
  namedWindow( anamorphosis, CV_WINDOW_AUTOSIZE );

  //Generate the file based on the output Matrix
  imwrite( "3-3.jpg", output);

  //Show the warped image to GUI window
  imshow( anamorphosis, output );

  //Exit on users Keyboard input
  waitKey(0);
  return 0;
}

//
//Function to map the new Image based on the index generated here
//Here's where where we need to observe original image as polar
//and somehow convert it to Cartesian
//
//
void MapIndex( void )
{
  const float hRows = image.rows/2;
  float angle, r;

  for( int y = 0; y < image.rows; y++ )
  { for( int x = 0; x < image.rows; x++ )
    {
      //Convert the image from raster form to Cartesian with 4 Quadrants
      float newX = (x - hRows);
      float newY = (y - hRows);
      
      //Get the theta of the polar representation
      //This will represent as Y axis
      angle=atan2(newY, newX);
      
      //Make the angle starts from 0 to 2PI instead of negative value
      if (angle < 0) {angle = angle+2*M_PI;}

      //Convert radian to degree, rotate 180 degree and normalize the angle
      angle = angle *180/M_PI;
      angle = fmod((angle+180),360);
      angle = angle*(image.cols-2)/360;

      //Get the radius of polar representation
      //Notice the ellipse formula here due to task b, 
      //which somehow conver the image to "torus" or ellipse with hole
      r=sqrt(pow(newX,2)/((10+leanX)/10)+pow(newY,2)/((10+leanY)/10));
      
      //Point the y to angle and x axis to radius
      //The HoleRadius is to create a hole in the middle of image
      IndexX.at<float>(y,x) = angle;
      IndexY.at<float>(y,x) = 2*(hRows-r)+HoleRadius;
      
    }
  }  
}