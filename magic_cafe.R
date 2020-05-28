#!/usr/bin/env Rscript

library <- function(...) {
  suppressPackageStartupMessages(base::library(...))
}
library(tidyverse)
library(rvest)
library(glue)

post2youtube <- function(post_url) {
  h <- read_html(post_url)

  h %>%
    html_nodes(".w90 .w100") %>%
    html_text() %>%
    str_trim() %>%
    tibble(text = .) %>%
    mutate(text = str_extract(text, "http.*youtube.*\\b")) %>%
    drop_na() %>%
    pull(text)
}

# ----

i <- 0
INDEX <- 30 * 0
MAGIC_CAFE_HOST <- "https://www.themagiccafe.com/forums"
MAGIC_CAFE_CHANNEL_WORKERS <- glue::glue("https://www.themagiccafe.com/forums/viewforum.php?forum=2&start={INDEX}")
MAGIC_CAFE_URL <- "https://www.themagiccafe.com/forums/viewtopic.php?topic=697959&forum=2"


# Worker Channel ----

chanel_page <- read_html(MAGIC_CAFE_CHANNEL_WORKERS)
df <- chanel_page %>%
  html_nodes(".nowrap+ .bgc2 .b") %>%
  html_attr("href") %>%
  tibble(url = .) %>%
  mutate(url = glue("{MAGIC_CAFE_HOST}/{url}")) %>%
  mutate(link = map(url, post2youtube))

# Parsing a Single Page ---

df %>%
  unnest(cols = c(link)) %>%
  format_tsv() %>%
  cat(sep = "\n")
