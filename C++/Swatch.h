
// knitting gauge calculator
#ifndef SWATCH_H
#define SWATCH_H

#include <iostream>
#include <optional>
#include <cmath>
#include <numbers>
#include "Shape.h"

class Swatch {

public: 
    
    Swatch();                                                // class constructor
    Swatch(float X, float Y, int Nsts, int Nrows, float needle_size);           // swatch dimensions and num of stitches
    ~Swatch();                                               // destructor (no need for virtual: it should not inherit from anything)

    /* *************************
       **   member functions  **
       *************************
    */
    // _________ Swatch __________
    float getX() const {return fX;};
    float getY() const {return fY;};

    int getNsts() const {return fNsts;};
    int getNrows() const {return fNrows;};

    float TensionFactor_sts(float sts_expected, float sts_actual);
    float TensionFactor_len(float length_actual, float length_expected);

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

    // convertion to mm or m
    static float toMillimiters(float meters);
    static float toMeters(float millimiters);

    float g_h() const;
    float g_v() const;
    float sts_in_Area(const Shape& region, float g_h, float g_v);
    float Area_in_sts(float Xsts, float Ysts, float g_h, float g_v);
    float linear_rho(float Mass_ball, float Length_ball);
    // inverse functions of density
    float inWeight(float lenght, float rho);
    float inLength(float mass, float rho);
    // length/weight needed to knit a number of stitches = tot_sts
    ////// float yarn_length_required(float tot_sts, float tension = 1.0f);
    ////// float yarn_length_required_with_needle(float tot_sts, float needle_size, float tension = 1.0f);
    // number of stitches knittable with a given length
    float sts_in_length(float length, float tension = 1.0f);
    float sts_in_length_with_needle(float needle_size, float length, float tension = 1.0f);
    

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

