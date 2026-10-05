
#include <iostream>
#include <cmath>
#include <optional>
#include <numbers>
#include "Swatch.h"
#include "Shape.h"


Swatch::Swatch():
    fX(0),
    fY(0),
    fNsts(0),
    fNrows(0),
    fSize(0)
    {
        // default constructor
    }

Swatch::Swatch(float X, float Y, int Nsts, int Nrows, float needle_size):
    fX(X),
    fY(Y),
    fNsts(Nsts),
    fNrows(Nrows),
    fSize(needle_size)
    {
        // std constructor
}

float Swatch::TensionFactor_sts(float sts_expected, float sts_actual){
    if( sts_actual <= 0){
        throw std::invalid_argument("The number of actual stitches must be greater than zero.");
    }
    return sts_expected/sts_actual;
}

// this function i
float Swatch::TensionFactor_len(float length_actual, float length_expected){
    if( length_expected <= 0){
        throw std::invalid_argument("The first argument must be greater than zero.");
    }
    return length_actual/length_expected;
}

float Swatch::toMillimiters(float meters){
    return meters*1000.0f;
}

float Swatch::toMeters(float millimiters){
    return millimiters/1000.0f;
}

float Swatch::g_h() const{
    return fX/fNsts;
}

float Swatch::g_v() const{
    return fY/fNrows;
}

float Swatch::sts_in_Area(const Shape& region, float g_h, float g_v){
    return region.Area() / (g_h * g_v);
}
// to be fixed
float Swatch::Area_in_sts(float Xsts, float Ysts, float g_h, float g_v){
    return (Xsts * Ysts) *(g_h * g_v);
}
// length has to be in mm!!
float Swatch::linear_rho(float Mass_ball, float Length_ball){
    return Mass_ball/Length_ball;
}

float Swatch::inWeight(float length, float rho){
    float mass = rho * length;
    return mass;
}

float Swatch::inLength(float mass, float rho){
    float length = mass / rho;
    return length;
}
// everything has to be in mm!!
// if the user doesn't insert a needle size, it takes the object's value
/*float Swatch::yarn_length_required(float tot_sts, float tension){
    return yarn_length_required_with_needle(tot_sts, fSize, tension);
}

// everything has to be in mm!!
float Swatch::yarn_length_required_with_needle(float tot_sts, float needle_size, float tension){
    float R = needle_size/2;              // size is the needle's diameter
    float length_st = 3 * std::numbers::pi * R * tension;
    float tot_length = length_st*tot_sts;
    return tot_length;
}*/
// everything has to be in mm!!
float Swatch::sts_in_length(float length, float tension){
    return sts_in_length_with_needle(fSize, length, tension);
}
// everything has to be in mm!!
float Swatch::sts_in_length_with_needle(float needle_size, float length, float tension){
    float R = needle_size/2;
    float length_st = 3 * std::numbers::pi * R * tension;
    if( length_st == 0){
        throw std::invalid_argument("Either Needle_size or Tension is null. Cannot divide by zero.");
    }
    float num_sts = length / length_st;             
    return num_sts;
}

Swatch::~Swatch(){
    // default destructor
}