require(RSelenium)
require(shiny)
require(miniUI)
require(futile.logger)
library(lubridate)
library(hrbrthemes)
library(rvest)
library(tidyverse)
library(stringr)

get_remdr <- function(url=NULL, round_trip=FALSE) {
  remDr <- remoteDriver(remoteServerAddr = "localhost", port = 4446L, browserName = "chrome")
  remDr$open()
  if(!is.null(url)) {
    flog.info("Navigating to %s", url)
    remDr$navigate(url)
    Sys.sleep(1)
  }
  if(round_trip) {
    webElem <- remDr$findElement("css", "body")
    webElem$sendKeysToElement(sendKeys = list(key="end"))
    webElem$sendKeysToElement(sendKeys = list(key="home"))
  }
  remDr
}
s <- function(rd=NULL) {
  if(is.null(rd)) {
    remDr$screenshot(display=TRUE)
  }  else {
    rd$screenshot(display=TRUE)
  }

}

get_password <- function() {
  ui <- miniPage(
    gadgetTitleBar("Please enter your password"),
    miniContentPanel(
      passwordInput("password", "")
    )
  )

  server <- function(input, output) {
    observeEvent(input$done, {
      stopApp(input$password)
    })
    observeEvent(input$cancel, {
      stopApp(stop("No password.", call. = FALSE))
    })
  }

  runGadget(ui, server, viewer = dialogViewer("Password", height = 200))
}

login <- function(remDr, id, password=get_password(), 
                  css_username="#id_username", css_password="#id_password") {
  webElem <- remDr$findElement(using="css", value = css_username)
  webElem$sendKeysToElement(list(id))
  webElem <- remDr$findElement(using="css", value = css_password)
  suppressWarnings(webElem$sendKeysToElement(list(password, key = "enter")))
}


read_html_remdr <- function(remDr) {
  remDr$getPageSource()[[1]] %>%
    read_html()
}

navigate_html <- function(remDr, url, sleep=3) {
  remDr$navigate(url)
  Sys.sleep(sleep)
  read_html_remdr(remDr)
}

find_elem <- function(remDr, selector) {
  remDr$findElement("css", selector)
}
get_elem_text <- function(webElem) {
  webElem$getElementText()[[1]]
}
click <- function(webElem) {
  webElem$clickElement()
}

do_login <- function(r, url) {
  r$navigate(url)
  creds <- read_lines("~/src/alee/secrets.py") %>%
    str_split(" = ") %>%
    map(function(x) x[2]) %>%
    gsub("'","",.)

  login(remDr = r, id = creds[1], password = creds[2])
}
