from Constants import QUADRATIC_FORWARD_RMS, CUBIC_FORWARD_RMS, DATA_EXT, DATA_PREC, EXACT_CUBIC_CONSTANT
from LoewnerRunFactory import LoewnerRunFactory
from numpy import square, mean, array, savetxt, absolute
from math import sqrt

class RootMeanSquareError:

    def __init__(self, start_time, final_time, outer_points, inner_points, resolutions):

        # Set the time parameters for the root mean sqaure comparisons
        self.start_time = start_time
        self.final_time = final_time

        # Set the resolution for the root mean sqaured comparisons
        self.outer_points = outer_points
        self.inner_points = inner_points

        # Set the different resolutions that will be used to calculate the RMS
        self.resolutions = resolutions

        # Prevent the individual runs from compiling and saving plots and data
        dont_compile = False
        dont_save_data = False
        dont_save_plot = False

        # Create a LoewneRun factory for generaring LoewnerRuns that can be used to determine RMS
        self.rms_factory = LoewnerRunFactory(start_time,final_time,outer_points,inner_points,dont_compile,dont_save_plot,dont_save_data)

    def calculate_rms(self, array_a, array_b):

        diff = array_a - array_b
        return sqrt(mean(square(absolute(diff))))

    def quadratic_forward_error(self, points=None):

        # Create a list of driving functions that have an exact solution for the quadratic forward case
        exact_solutions = self.rms_factory.create_exact_quadratic_forward()

        # Use the resolutions that were created during class initialisation if no others are given
        if points == None:
            points = self.resolutions

        # Iterate through the exact solutions
        for exact_sol in exact_solutions:

            # Declare an empty list for the error values
            rms_list = []

            # Carry out the exact solution
            exact_sol.exact_quadratic_forward_loewner()

            # Create a list of LoewnerRuns corresponding with exact solution that have different inner resolutions
            approx_solutions = self.rms_factory.vary_inner_res(exact_sol.index, points)

            # Iterate through the approx solutions
            for approx_sol in approx_solutions:

                # Execute the approx solutions
                approx_sol.quadratic_forward_loewner()

                print("Finished solution with inner res = " + str(approx_sol.inner_points) + " for driving function " + str(approx_sol.name))

                # Calculate the root mean sqaure error
                rms = self.calculate_rms(exact_sol.exact_quadratic_forward, approx_sol.forward_results)

                # Add the RMS value to the list
                rms_list.append([approx_sol.inner_points, rms])

            # Create a filename for the error values
            filename = QUADRATIC_FORWARD_RMS + str(exact_sol.index) + "-RMS" + DATA_EXT

            # Save the error values to the filesystem
            savetxt(filename, array(rms_list), fmt=DATA_PREC)

    def cubic_forward_error(self, points=None):

        # Create a list of driving functions that have an exact solution for the quadratic forward case
        exact_solutions = self.rms_factory.create_exact_cubic()

        # Use the resolutions that were created during class initialisation if no others are given
        if points == None:
            points = self.resolutions

        # Iterate through the exact solutions
        for exact_sol in exact_solutions:

            # Declare empty lists for the error values
            rms_list_a = []
            rms_list_b = []

            # Carry out the exact solution
            exact_sol.exact_cubic_forward_loewner()

            # Create a list of LoewnerRuns corresponding with exact solution that have different inner resolutions
            approx_solutions = self.rms_factory.vary_inner_res(exact_sol.index,points, constant=EXACT_CUBIC_CONSTANT)

            # Iterate through the approx solutions
            for approx_sol in approx_solutions:

                # Execute the approx solutions
                approx_sol.cubic_forward_loewner()

                print("Finished solution with inner res = " + str(approx_sol.inner_points) + " for driving function " + str(approx_sol.name))

                # Calculate the root mean sqaure error
                rms_a = self.calculate_rms(exact_sol.exact_cubic_sol_a, approx_sol.cubic_results_a)
                rms_b = self.calculate_rms(exact_sol.exact_cubic_sol_b, approx_sol.cubic_results_b)

                # Add the RMS value to the list
                rms_list_a.append([approx_sol.inner_points, rms_a])
                rms_list_b.append([approx_sol.inner_points, rms_b])

            # Create a filename for the error values
            filename_a = CUBIC_FORWARD_RMS + str(exact_sol.index) + "-RMS-A" + DATA_EXT
            filename_b = CUBIC_FORWARD_RMS + str(exact_sol.index) + "-RMS-B" + DATA_EXT

            # Save the error values to the filesystem
            savetxt(filename_a, array(rms_list_a), fmt=DATA_PREC)
            savetxt(filename_b, array(rms_list_b), fmt=DATA_PREC)

