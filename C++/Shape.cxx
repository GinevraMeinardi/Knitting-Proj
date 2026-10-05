#include <iostream>
#include <cmath>
#include <optional>
#include <numbers>
#include "Shape.h"

// ________ Rectangle functions ________

Rectangle :: Rectangle(float x, float y):
    fX(x),
    fY(y)
    {}

float Rectangle::Area() const {
    return fX * fY;
}

// __________ Circular Slice ____________

CircularSlice::CircularSlice(float r):
    CircularSlice(r, 360.0f) {}

CircularSlice::CircularSlice(float r, float deg):
    fR(r),
    fDeg(deg)
    {}

float CircularSlice::Area() const {
    float rad = fDeg * std::numbers::pi_v<float> / 180.0f;              // conversion to radians
    return 0.5f * rad * fR * fR;                                    // 0.5 because 360 -> 2Pi but the area is piR^2 not 2PiR^2
}

// __________ Trapezoid __________

Trapezoid::Trapezoid(float a, float b, float h):
    fA(a),
    fB(b),
    fH(h)
    {}

float Trapezoid::Area() const {
    return 0.5f * (fA + fB) * fH;
}

// __________ Triangle __________

Triangle::Triangle(float b, float h):
    fB(b),
    fH(h)
    {}
float Triangle::Area() const {
    return 0.5f * fB * fH;
}