#include <SFML/Graphics.hpp>
#include <iostream>
#include <cmath>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <limits>

// Global constants
const int PIXEL_DIMENSION = 400;
const int NUM_POINTS = 6;
const float CIRCLE_RADIUS = 3.0f;
const unsigned int FRAME_RATE = 60;
const double INIT_P = -5.0;
const double FINAL_P = 100.0;
const double SLOW_INCREMENT = 0.01;
const double FAST_INCREMENT = 0.05;
const double RAPID_INCREMENT = 1.0;
const double SLOW_PAST_P = 0.0;
const double FAST_PAST_P = 2.5;
const double RAPID_PAST_P = 5.0;

// Function to generate a random number in a given range
double randomInRange(double start, double stop) {
    double rangeWidth = stop - start;
    double noncenteredRandom = static_cast<double>(rand()) / RAND_MAX * rangeWidth;
    return noncenteredRandom + start;
}

int main() {
    // Initialize random seed
    srand(static_cast<unsigned>(time(0)));

    sf::RenderWindow window(sf::VideoMode(PIXEL_DIMENSION, PIXEL_DIMENSION), "Voronoi Diagram");
    window.setFramerateLimit(FRAME_RATE);

    double p = INIT_P;
    double increment = FAST_INCREMENT;

    std::vector<sf::Vector2f> points(NUM_POINTS);
    std::vector<sf::Color> colors(NUM_POINTS);
    for (int i = 0; i < NUM_POINTS; i++) {
        points[i].x = randomInRange(0, PIXEL_DIMENSION);
        points[i].y = randomInRange(0, PIXEL_DIMENSION);
        colors[i] = sf::Color(
            static_cast<sf::Uint8>(randomInRange(0, 255)),
            static_cast<sf::Uint8>(randomInRange(0, 255)),
            static_cast<sf::Uint8>(randomInRange(0, 255))
        );
    }

    sf::Clock clock;
    sf::Time timePerFrame = sf::seconds(1.0f / FRAME_RATE);

    while (window.isOpen() && p < FINAL_P) {
        sf::Time elapsedTime = clock.restart();

        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        window.clear();

        std::vector<sf::Vertex> pixels;
        pixels.reserve(PIXEL_DIMENSION * PIXEL_DIMENSION);

        std::cout << "The p used for Minkowski Distance: " << p << std::endl;

        for (int i = 0; i < PIXEL_DIMENSION; i++) {
            for (int j = 0; j < PIXEL_DIMENSION; j++) {
                double closestDistance = std::numeric_limits<double>::max();
                int closestIndex = -1;
                for (int k = 0; k < NUM_POINTS; k++) {
                    double absX = std::abs(points[k].x - i);
                    double absY = std::abs(points[k].y - j);
                    double sum = std::pow(absX, p) + std::pow(absY, p);
                    double distance = std::pow(sum, 1 / p);
                    if (distance < closestDistance) {
                        closestDistance = distance;
                        closestIndex = k;
                    }
                }
                sf::Vertex pixel(sf::Vector2f(i, j), closestIndex == -1 ? sf::Color::Black : colors[closestIndex]);
                pixels.push_back(pixel);
            }
        }

        window.draw(&pixels[0], pixels.size(), sf::Points);

        for (int i = 0; i < NUM_POINTS; i++) {
            sf::CircleShape point(CIRCLE_RADIUS);
            point.setPosition(points[i].x - CIRCLE_RADIUS, points[i].y - CIRCLE_RADIUS);
            point.setFillColor(sf::Color::Red);
            window.draw(point);
        }

        window.display();

        p += increment;

        sf::Time timeToSleep = timePerFrame - clock.getElapsedTime();
        if (timeToSleep > sf::Time::Zero) {
            sf::sleep(timeToSleep);
        }

        if (p > SLOW_PAST_P) {
            increment = SLOW_INCREMENT;
        }
        if (p > FAST_PAST_P) {
            increment = FAST_INCREMENT;
        }
        if (p > RAPID_PAST_P) {
            increment = RAPID_INCREMENT;
        }
    }

    return 0;
}
