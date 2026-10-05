
// knitting gauge calculator
#ifndef GAUGE_H
#define GAUGE_H

#include <iostream>
#include <optional>
#include <cmath>
#include <numbers>
#include "Shape.h"

class Gauge {

public: 
    
    Gauge();                                                // class constructor
    Gauge(float X, float Y, int Nsts, int Nrows, float needle_size);           // to calculate the gauge we need swatch dimensions and num of stitches
    ~Gauge();                                               // destructor (no need for virtual: it should not inherit from anything)

    /* *************************
       **   member functions  **
       *************************
    */
    // _________ Swatch __________
    float getX() const {return fX;};
    float getY() const {return fY;};

    int getNsts() const {return fNsts;};
    int getNrows() const {return fNrows;};

    float TensionFactor(int sts_expected, int sts_actual);

    // ____________ Area to cover ___________
    void setA_x(float area_width) { fA_x = area_width;};
    void setA_y(float area_height) { fA_y = area_height;};

    bool hasA_x() const { return fA_x.has_value();};
    bool hasA_y() const { return fA_y.has_value();};

    std::optional<float> getA_x() const {return fA_x;};
    std::optional<float> getA_y() const {return fA_y;};

    // _____________ Yarn _____________
    void setLength(float length) { fLength_b = length;};
    void setWeight(float weight) { fMass_b = weight;};

    bool hasLength() const { return fLength_b.has_value();};
    bool hasWeight() const { return fMass_b.has_value();};

    std::optional<float> getWeight() const {return fMass_b;};
    std::optional<float> getLength() const {return fLength_b;};

    float getNeedle_size() const {return fSize;};

    float g_h(float x, int sts_num);
    float g_v(float y, int rows_num);
    float sts_in_Area(const Shape& region, float g_h, float g_v);
    float linear_rho(float length_ball, float mass_ball);
    // inverse functions of density
    float inWeight(float lenght, float rho);
    float inLength(float mass, float rho);
    // length/weight needed to knit a number of stitches = tot_sts
    float yarn_length_required(float tot_sts, float needle_size, float tension = 1.0f);
    float yarn_weight_required(float total_length, float rho);
    // number of stitches knittable with a given length
    float sts_in_length(float needle_size, float length);
    

    /* *************************
       **   member variables  **
       *************************
    */
   private:

    // swatch dimensions
    float fX;                         // [cm]
    float fY;                         // [cm]
    int fNsts;
    int fNrows;
    // area dimensions
    std::optional<float> fA_x;        // [cm]
    std::optional<float> fA_y;        // [cm]
    // yarn ball variables
    std::optional<float> fLength_b;   // [m]
    std::optional<float> fMass_b;     // [g]
    // needle dimensions
    float fSize;                      // [mm]
    

};

#endif

ah okay, no I was used to root and I looked at an old readme file for a project which is the template i'm using for this project but I forgot about root oosh! Is there a way to create a makefile? would it be useful? I think it'd be really interesting and useful for my personal coding skills