library(shiny)
library(shinyFiles)
library(shinythemes)
library(reticulate)

# Define UI ----
ui <- fluidPage(theme = shinytheme('darkly'),

  titlePanel(
    "Hello!"
  ),

  sidebarLayout(
    sidebarPanel(
      fluidRow(
        p("1. Upload image (jpg/png for now):"),
        p("2. Submit the file into the program "),
        p("3. Download the resulting image (.png) file using the download button "),
        p("4. Name it what you want (leave the .png) and download it where you want, default is the downloads folder"),
        br(),
        p("May take a few seconds")
      )
    ),

    mainPanel(

      fluidRow(
        fileInput("uploadedData", "Upload input file here (.jpg/png)", accept = c(".jpg", "png")),
        actionButton("submit1", "Submit", icon = icon("arrow-alt-circle-right")),
        textOutput("dataValue")
      ),

      tags$br(),
      fluidRow(
        downloadButton("dl", "Download")
      )
    )
  )
)

server <- function(input, output) {
  #get the path of the file submitted to use in the function call
  inputPathVar <- reactive({
    input$uploadedData$datapath
  })

  # Submission Check
  output$dataValue <- renderText({
    req(input$submit1)
    return(isolate("File submitted; Ready for download"))
  })

  # Download Button  
  output$dl <- downloadHandler(
    filename = function() { "cropped.png" }, # default name
    content = function(file) {
      showModal(modalDialog("Downloading", footer = NULL)) # shows the "Downloading" menu
      on.exit(removeModal())
      # the file being made to download
      source_python("crop.py")
    }
  )
}


# Run the app ----
shinyApp(ui = ui, server = server)