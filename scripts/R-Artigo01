# ==============================================================================
# SCRIPT COMPLETO: ANÁLISES R E ECONOMETRIA (ARTIGO DE ADMINISTRAÇÃO / ARTIGO 1)
# AUTOR: BRENO DOS SANTOS RODRIGUES (2026) - UFPR
# ==============================================================================

# 1. CARREGAR BIBLIOTECAS
library(readxl)
library(stringr)
library(lubridate)
library(dplyr)
library(writexl)
library(car)
library(lmtest)
library(nortest)
library(estimatr) # Essencial para erros-padrão robustos HC3

# 2. CARREGAR DADOS
# Ajuste para o caminho do seu arquivo de dados processados
caminho_banco <- "dados_nordeste_processado.xlsx" 
df <- read_excel(caminho_banco)

# 3. PRÉ-PROCESSAMENTO E CRIAÇÃO DE VARIÁVEIS
df$num_fotos <- ifelse(is.na(df$review_media) | df$review_media == "", 0, str_count(df$review_media, ",") + 1)

# Extração geográfica
df$info_destino_raw <- str_remove(str_extract(df$query, "Reviews-.*\\.html"), "Reviews-")
df$info_destino_raw <- str_remove(df$info_destino_raw, "\\.html")
df$Nome_Atracao <- str_replace_all(str_extract(df$info_destino_raw, "^[^-]+"), "_", " ")
df$Cidade <- NA_character_
df$Estado <- NA_character_

for (i in seq_along(df$info_destino_raw)) {
  if (!is.na(df$info_destino_raw[i])) {
    partes <- str_remove(df$info_destino_raw[i], "^[^-]+-")
    if (str_detect(partes, "_State_of_")) {
      split <- str_split(partes, "_State_of_")[[1]]
      df$Cidade[i] <- str_replace_all(split[1], "_", " ")
      df$Estado[i] <- ifelse(length(split) > 1, str_replace_all(split[2], "_", " "), NA)
    } else {
      df$Cidade[i] <- str_replace_all(partes, "_", " ")
    }
  }
}
df <- df %>% dplyr::select(-info_destino_raw)

# Conversão de datas e variáveis métricas
df$reviews <- as.numeric(df$reviews)
df$review_date <- as.Date(parse_date_time(str_trim(str_replace(df$review_date, "Feita em ", "")), orders = c("d B Y", "dmy", "ymd"), locale = "pt_BR", truncated = 3))
df$owner_response_date_final <- as.Date(parse_date_time(str_trim(str_replace(df$owner_response_date, "Feita em ", "")), orders = c("d B Y", "dmy", "ymd"), locale = "pt_BR", truncated = 3))
df$has_owner_response <- !is.na(df$owner_response) & df$owner_response != ""

# Variáveis do Estudo
df$review_text_clean <- str_remove_all(str_remove_all(str_remove_all(tolower(df$review_text), "http[s]?://\\S+"), "[[:punct:]]"), "[[:digit:]]")
df$Length_of_review <- str_count(df$review_text_clean, "\\w+")
df$Review_Freshness <- as.numeric(difftime(max(df$review_date, na.rm = TRUE), df$review_date, units = "days"))
df <- df %>% group_by(author_title) %>% mutate(User_Activity_in_Sample = n()) %>% ungroup()
df$owner_response_freshness <- as.numeric(difftime(df$owner_response_date_final, df$review_date, units = "days"))
df$owner_response_freshness[df$owner_response_freshness < 0] <- NA

# 4. ANÁLISE DESCRITIVA E TESTES PRELIMINARES
summary(df[, c("review_rating", "Length_of_review", "num_fotos", "Review_Freshness", "User_Activity_in_Sample", "owner_response_freshness")])

# 5. MODELO DE REGRESSÃO COM ERROS-PADRÃO ROBUSTOS (HC3)
# Utiliza lm_robust do pacote estimatr para garantir robustez contra heteroscedasticidade
modelo_robust <- lm_robust(review_rating ~ Length_of_review + num_fotos + Review_Freshness + 
                             User_Activity_in_Sample + has_owner_response + Cidade, 
                           data = df, se_type = "HC3")
summary(modelo_robust)

# 6. TESTES DE ROBUSTEZ ADICIONAIS
modelo_padrao <- lm(review_rating ~ Length_of_review + num_fotos + Review_Freshness + 
                      User_Activity_in_Sample + has_owner_response + Cidade, data = df)
vif(modelo_padrao)
bptest(modelo_padrao)

# 7. TESTE QUI-QUADRADO (SILÊNCIO GERENCIAL)
df$perfil_eWOM <- cut(df$review_rating, breaks = c(0, 2.5, 3.5, 5.1), labels = c("Detratores", "Neutros", "Promotores"))
tabela_contigencia <- table(df$perfil_eWOM, df$has_owner_response)
chisq.test(tabela_contigencia)
print(round(prop.table(tabela_contigencia, margin = 1) * 100, 2))

# 8. EXPORTAÇÃO (Opcional)
# write_xlsx(df, "resultado_processado_dissertacao.xlsx")
