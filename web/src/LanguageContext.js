import React from "react"

const LanguageContext = React.createContext("en")

export const LanguageProvider = LanguageContext.Provider
export const LanguageConsumer = LanguageContext.Consumer
export default LanguageContext


