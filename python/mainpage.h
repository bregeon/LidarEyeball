// Mainpage for doxygen

/** @mainpage package LidarEyeball
 *
 * @authors J. Bregeon
 *
 * @section intro Introduction
 *
 *  LidarEyeball package to handle HESS Lidar runs
 *
 *  - @ref pLidarRun : pLidarRun.py contains the pLidarRun class to analyze
*     Lidar data
 *  - @ref pLidarRunPlotter : pLidarRunPlotter.py contains the pLidarRunPlotter
*     class to plot results from the Lidar analysis done with a pLidarRun object
 *  - pRayleigh.py and pRayleighPlotter.py estimate the Rayleigh scattering
 *    contribution
 *  - @ref pTriggerRate : pTriggerRate.py estimates a simple trigger rate from
*     HESS camera ROOT files
 *  - pSashInterface.py : interface to HESS ROOT Sash data format (Sash::DataSet)
 *  - pDataInterface.py : interface to data on disk by run number, file path or
 *    directory
 *  - @ref tools : toolBox.py
 *
 * @section pLidarRun Lidar Data analysis
 *
 * Lidar data analysis
 * 
 * @section pLidarRunPlotter Analysis plotter
 *
 * Lidar data analysis plotter
 *
 * @section pTriggerRate Camera Data analysis for Trigger rate
 *
 * Basic HESS camera data analysis to estimate a (corrected) trigger rate
 *
 * @section tools Lidar analysis tool box
 *
 * toolBox.py contains a set of functions to do stuff
 *
 * <hr>
 * @todo pTriggerRate.py
 *  - be able to combine multiple runs in one plot
 *  - fix get minimum and maximum time stamps in fillRawTriggerRate
 * @todo pSashInterface.py
 *  - really create a Sash::DatSet given a run number or a list of files
 * @todo pDataInterface.py
 *  - either give back a list of files for a run number
 *  - or give back Sash::DataSet for a given run number
*/

