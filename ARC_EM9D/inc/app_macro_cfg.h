/*
 * aiot_facedetect_macro_cfg.h
 *
 *  Created on: 2019/8/2
 *      Author: 902447
 */

#ifndef APP_MACRO_CFG_H_
#define APP_MACRO_CFG_H_

/*APP Compiler flag Selection*/
//#define APPTYPE_HUMANDET_CDM
//#define APPTYPE_HUMANDET_DIGITAL_PIR
//#define APPTYPE_HUMANDET_ANALOG_PIR
//#define APPTYPE_OCCUPANCY_SENSOR
#define APPTYPE_FACE_DETECT_ALLON
//#define APPTYPE_FACE_DETECT_CDM
//#define APPTYPE_HUMAN_DETECT_CDM
//#define APPTYPE_ALGO_DETECT_ANALOG_WAKEUP
//#define APPTYPE_ALGO_DETECT_SENSORMD_WAKEUP
//#define APPTYPE_ALGO_DETECT_PERIODICAL_WAKEUP_QUICKBOOT

#define APP_VERSION   "1.0.0"
#define SUPPORT_CPU_SLEEP_AT_CAPTURE
#define SENSOR_STROBE_REQ     0
/*TODO need change*/
#define FLASH_APPCFG_BASEADDR    0xB9000
#define FLASH_ALGOCFG_BASEADDR    0xBB000

//#define TEST_TFLITEMICRO_CODE_ONLY

#define MAX_RTC_NOT_RECAP_ERR_RETRY_CNT     	100
#define MAX_RTC_NOT_RECAP_ERR_REBOOT_CNT     	200

#define USE_TICK 1


/*Sensor Cfg*/
#define MAX_RECONFIG_SENSOR_TIME     5
//#define NONEAOS_TOGGLE_STREAM_STANDBY

/*Error Retry Count*/
#define MAX_HW5x5JPEG_ERR_RETRY_CNT     10


#define SENOSR_TOGGLE_STREAM_LIMITATION_MS  20
/////////////////////

///////////////Transfer//////////
//#define SUPPORT_SPI_SOC_TRANSFER
// #define SUPPORT_SPI_PC_TRANSFER_ENC_EVERYFRAME      /* JPEG */
#define SUPPORT_SPI_PC_TRANSFER_ENC_EVERYFRAME_META      /* JPEG +META*/
//#define SUPPORT_SPI_PC_TRANSFER_RAW
//////////////////////////////////

//#define SUPPORT_PRINT_CFG_HEADER
//#define SUPPORT_PRINT_CFG_CONTENT

//#define SUPPORT_TEST_MODE
//#define TEST_FACE_FRAME_NO   6

#define NO_ALGO_SIM    0
//#define SIM_I2C_CHANGE_STATE
#define SIM_ADC_RTC_PERIOD  30000
//#define APP_DEBUG_PRINT
#endif /* APP_MACRO_CFG_H_ */
