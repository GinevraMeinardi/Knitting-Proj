
// different shapes area calculator

#ifndef SHAPE_H
#define SHAPE_H

#include <iostream>
#include <cmath>
#include <optional>
#include <numbers>

class Shape{

public:

    virtual float Area() const = 0;               // function
    virtual ~Shape() = default;                   // destructor
};

/* building a constructor with virtual allows 
    to use dynamic binding
*/
// ________________________________________

class Rectangle : public Shape{

public:

    Rectangle(float x, float y);
    float Area() const override;

private:

    float fX, fY;
};
// ________________________________________

class CircularSlice : public Shape{

public:
    // the degrees are default to 360 full circle
    CircularSlice(float r);
    // if you want just a slice
    CircularSlice(float r, float deg);
    float Area() const override;          

private:

    float fR;                   // [cm]
    float fDeg;                 // [°]
};
// ________________________________________

class Trapezoid : public Shape{

public:
    Trapezoid(float a, float b, float h);
    
    float Area() const override;

private:

    float fA, fB, fH;
};
// ________________________________________

class Triangle : public Shape{

public:
/* maybe i'll need a function for every kind of triangle there is
   because the geometrical shape depends on the kind of increases
   and decreases, but for now, just calculating the area, 
   the general shape works fine
*/
    Triangle(float b, float h);
    
    float Area() const override;
    
private:

    float fB, fH;
};

#endif