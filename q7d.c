/* Standard includes. */
#include <stddef.h>

/* Local includes. */
#include "console.h"

/* FreeRTOS kernel includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"
#include "queue.h"

SemaphoreHandle_t mutex;
QueueHandle_t xInputQueue;

#define MAX_LINE_LENGTH 64
#define INPUT_QUEUE_LENGTH 2

typedef struct {
  char const * message;
  TickType_t delay;
} TaskData_t;

static void prvPrintTask( void * pvParameters ) {
  TaskData_t const * const data = pvParameters;
  while( 1 )
  {
    vTaskDelay( data->delay );
    xSemaphoreTake( mutex, portMAX_DELAY );
    console_write( data->message );
    xSemaphoreGive( mutex );
  }
}

static void prvInputTask( void * pvParameters ) {
  char line[ MAX_LINE_LENGTH ];
  ( void ) pvParameters;

  while( 1 )
  {
    if( xQueueReceive( xInputQueue, line, portMAX_DELAY ) == pdPASS )
    {
      xSemaphoreTake( mutex, portMAX_DELAY );
      console_write( line );
      xSemaphoreGive( mutex );
    }
  }
}


void console_keyboard_ISR( void )
{
  static char buffer[ MAX_LINE_LENGTH ];
  static size_t index = 0;
  char c;
  BaseType_t xStatus;

  c = console->in_char;

  if( c == '\r' )
  {
    c = '\n';
  }

  if( index < ( MAX_LINE_LENGTH - 1U ) )
  {
    buffer[ index++ ] = c;
  }

  if( ( c == '\n' ) || ( index >= ( MAX_LINE_LENGTH - 1U ) ) )
  {
    buffer[ index ] = '\0';

    xStatus = xQueueSendToBackFromISR( xInputQueue, buffer, NULL );
    ( void ) xStatus;

    index = 0;
  }
}

void main( void )
{
  console_init( );
  mutex = xSemaphoreCreateMutex( );
  xInputQueue = xQueueCreate( INPUT_QUEUE_LENGTH, MAX_LINE_LENGTH * sizeof( char ) );
  TaskData_t taskData1 = { .message = "Message from Task 1\n", .delay = 250 };
  TaskData_t taskData2 = { .message = "Hello from Task 2\n", .delay = 600 };
  xTaskCreate( prvPrintTask, "Task 1", configMINIMAL_STACK_SIZE, &taskData1, tskIDLE_PRIORITY + 1, NULL );
  xTaskCreate( prvPrintTask, "Task 2", configMINIMAL_STACK_SIZE, &taskData2, tskIDLE_PRIORITY + 1, NULL );
  xTaskCreate( prvInputTask, "Input", configMINIMAL_STACK_SIZE, NULL, tskIDLE_PRIORITY + 2, NULL );
  console_IRQ_enable( IRQ_KEYBOARD );
  console_printf( "Program starting...\n" );
  vTaskStartScheduler( );
}
