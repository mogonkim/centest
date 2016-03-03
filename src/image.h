#pragma once
#include <memory>
#include <algorithm>
#include <cmath>
static float clamp_f(float min, float max, float x)
{
    return std::max(min,std::min(max,x));
}

namespace img {
	
	template <typename T, int C>
	struct Image {
		std::shared_ptr<T> data;
		int width, height;
		Image() : data(nullptr),width(0),height(0) {}
		Image(int width, int height) : data(new T[width*height*C], arr_d()),width(width),height(height) {}
		Image(int width, int height, T* d) : data(d, null_d()), width(width), height(height)  {}

		struct null_d { void operator ()(T const * p)	{ } };
		struct arr_d { void operator ()(T const * p)	{ delete[] p; } };
	    T sample(const float x, const float y, int chan) {
            auto pixX = [this](float x){ return (int)clamp_f(0.0f,(float)(width-1),std::round(x)); };
            auto pixY = [this](float y){ return (int)clamp_f(0.0f,(float)(height-1),std::round(y)); };

            auto xm = pixX(x-0.5f);
            auto xp = pixX(x+0.5f);
            auto ym = pixY(y-0.5f);
            auto yp = pixY(y+0.5f);
            auto ptr = data.get();

            auto tl = ptr[C*(ym*width+xm)+chan];
            auto tr = ptr[C*(ym*width+xp)+chan];
            auto bl = ptr[C*(yp*width+xm)+chan];
            auto br = ptr[C*(yp*width+xp)+chan];

            float dx = x - xm;
            float dy = y - ym;

            auto sample = tl*(1.f-dx)*(1.f-dy) + tr*dx*(1.f-dy) + bl*(1.f-dx)*dy + br*dx*dy;
            return (T)sample;
        }
    };

	template<typename T> using Img = Image<T, 1>;
}
