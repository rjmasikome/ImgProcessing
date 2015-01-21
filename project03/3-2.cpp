//
//  main.cpp
//  OpenCVBaseProject
//
//  Created by Muhammad Abduh on 12/31/14.
//  Copyright (c) 2014 Muhammad Abduh. All rights reserved.
//

#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdio.h>

using namespace cv;
using namespace std;

const int amp_slider_max_x = 100;
int amp_slider_x;
const int freq_slider_max_x = 100;
int freq_slider_x;
const int phase_slider_max_x = 200;
int phase_slider_x;

const int amp_slider_max_y = 100;
int amp_slider_y;
const int freq_slider_max_y = 100;
int freq_slider_y;
const int phase_slider_max_y = 200;
int phase_slider_y;

/// Matrices to store images
Mat img;
Mat img_new;
Mat img_dst;
Mat img_buf;

int amp_x = 0;
int freq_x = 0;
int ph_x = 0;
int amp_y = 0;
int freq_y = 0;
int ph_y = 0;

/**
 * @function process
 * @brief Process function
 */
void process()
{
    img_new = Mat::zeros(img.rows*2, img.cols*2, img.type());
    img_buf = Mat::zeros(img.rows*2, img.cols*2, img.type());
   
//    BASIC EQUATION
//----------------------------------------------------------------------
//    for (int x=0; x<img.rows; x++) {
//        const uchar* it = img.ptr<uchar>(x);
//        uchar* it_dest = img_new.ptr<uchar>(x);
//        for (int y=0; y<img.cols; y++)
//        {
//            float delta_x = amp_x * sin((y*freq_x*M_PI/180)- ph_x);
//            float delta_y = amp_y * sin((x*freq_y*M_PI/180)- ph_y);
//
//            uint8_t x_new = (uint8_t)delta_x + img.rows/2;
//            uint8_t y_new = (uint8_t)delta_y + img.cols/2;
//
//            if (x_new < img_new.rows || x_new > 0) {
//                if (y_new < img_new.cols || y_new > 0) {
//                    it_dest[y+y_new+x_new*img_new.cols] = it[y];
//                }
//            }
//        }
//    }
//----------------------------------------------------------------------
    
    for (int x=0; x<img.rows; x++) {
        const uchar* it = img.ptr<uchar>(x);
        uchar* it_dest = img_buf.ptr<uchar>(x);
        for (int y=0; y<img.cols; y++)
        {
            float delta_x = amp_x * sin((y*freq_x*M_PI/180)- ph_x);
            
            uint8_t x_new = (uint8_t)delta_x + img.rows/2;
            
            if (x_new < img_buf.rows || x_new > 0) {
                    it_dest[y+x_new*img_buf.cols] = it[y];
            }
        }
    }
    
    
    for (int x=img.rows/2-amp_x; x<amp_x+img.rows+img.rows/2; x++) {
        const uchar* it = img_buf.ptr<uchar>(x);
        uchar* it_dest = img_new.ptr<uchar>(x);
        for (int y=0; y<img.cols; y++)
        {
            float delta_y = amp_y * sin((x*freq_y*M_PI/180)- ph_y);
            
            uint8_t y_new = (uint8_t)delta_y + img.cols/2;
            
                if (y_new < img_new.cols || y_new > 0) {
                    it_dest[y+y_new] = it[y];
                }
        }
    }
    
    char txtbuf[20];

    sprintf(txtbuf, "Amplitude X : %d", amp_x);
    putText(img_new,txtbuf, Point(0,20), CV_FONT_NORMAL, 0.5, Scalar::all(255), 1,1);
    
    sprintf(txtbuf, "Frequency X : %d", freq_x);
    putText(img_new,txtbuf, Point(0,35), CV_FONT_NORMAL, 0.5, Scalar::all(255), 1,1);
    
    sprintf(txtbuf, "Phase     X : %d", ph_x);
    putText(img_new,txtbuf, Point(0,50), CV_FONT_NORMAL, 0.5, Scalar::all(255), 1,1);
    
    sprintf(txtbuf, "Amplitude Y : %d", amp_y);
    putText(img_new,txtbuf, Point(0,65), CV_FONT_NORMAL, 0.5, Scalar::all(255), 1,1);
    
    sprintf(txtbuf, "Frequency Y : %d", freq_y);
    putText(img_new,txtbuf, Point(0,80), CV_FONT_NORMAL, 0.5, Scalar::all(255), 1,1);
    
    sprintf(txtbuf, "Phase     Y : %d", ph_y);
    putText(img_new,txtbuf, Point(0,95), CV_FONT_NORMAL, 0.5, Scalar::all(255), 1,1);
    
    imshow("ImageProcessing", img_new);
    
}

/**
 * @function on_trackbar_var
 * @brief Callback for trackbar
 */
void on_trackbar_amp_x( int, void* )
{
    int amp_value = amp_slider_x;
    amp_x = amp_value;
    process();
}

void on_trackbar_freq_x( int, void* )
{
    freq_x = freq_slider_x;
    process();
}

void on_trackbar_phase_x( int, void* )
{
    int phase_value = phase_slider_x - 100;
    ph_x = phase_value;
    process();
}

void on_trackbar_amp_y( int, void* )
{
    int amp_value = amp_slider_y;
    amp_y = amp_value;
    process();
}

void on_trackbar_freq_y( int, void* )
{
    freq_y = freq_slider_y;
    process();
}

void on_trackbar_phase_y( int, void* )
{
    int phase_value = phase_slider_y - 100;
    ph_y = phase_value;
    process();
}


/**
 * @function main
 * @brief Main Function
 */
int main( int argc, char** argv )
{
    /// Read image ( same size, same type )
    img = imread("bauckhage.jpg", CV_LOAD_IMAGE_GRAYSCALE); //read the image data in the file "MyPic.JPG" and store it in 'img'

    if (img.empty()) //check whether the image is loaded or not
    {
        cout << "Error : Image cannot be loaded..!!" << endl;
        //system("pause"); //wait for a key press
        return -1;
    }
    
    /// Initialize values
    amp_slider_x = 0;
    freq_slider_x = 0;
    phase_slider_x = 100;
    amp_slider_y = 0;
    freq_slider_y = 0;
    phase_slider_y = 100;
    
//    process();
    /// Create Windows
    namedWindow("ImageProcessing", CV_WINDOW_NORMAL);
    
    /// Create Trackbars

    
    createTrackbar( "Amp X", "ImageProcessing", &amp_slider_x, amp_slider_max_x, on_trackbar_amp_x );
    
    createTrackbar( "Freq X", "ImageProcessing", &freq_slider_x, freq_slider_max_x, on_trackbar_freq_x );

    createTrackbar( "Phase X", "ImageProcessing", &phase_slider_x, phase_slider_max_x, on_trackbar_phase_x );
    
    createTrackbar( "Amp Y", "ImageProcessing", &amp_slider_y, amp_slider_max_y, on_trackbar_amp_y );
    
    createTrackbar( "Freq Y", "ImageProcessing", &freq_slider_y, freq_slider_max_y, on_trackbar_freq_y );
    
    createTrackbar( "Phase Y", "ImageProcessing", &phase_slider_y, phase_slider_max_y, on_trackbar_phase_y );
  

    on_trackbar_amp_x( amp_slider_x, 0 );
    on_trackbar_freq_x( freq_slider_x, 0 );
    on_trackbar_phase_x( phase_slider_x, 0 );
    on_trackbar_amp_y( amp_slider_y, 0 );
    on_trackbar_freq_y( freq_slider_y, 0 );
    on_trackbar_phase_y( phase_slider_y, 0 );

    /// Wait until user press some key
    waitKey(0);
    destroyAllWindows();
    return 0;
}