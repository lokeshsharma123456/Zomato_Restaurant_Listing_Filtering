package main

import (
	"encoding/csv"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/xuri/excelize/v2"
)

type Restaurant struct {
	RestaurantID     string `json:"Restaurant ID"`
	RestaurantName   string `json:"Restaurant Name"`
	Locality         string `json:"Locality"`
	Cuisines         string `json:"Cuisines"`
	AggregateRating  string `json:"Aggregate rating"`
	CountryCode      string `json:"Country Code"`
}
 
type CountryCode struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}


var restaurantMap map[string]Restaurant
var restaurantList []Restaurant

func loadCSVData(filePath string) {
	file, err := os.Open(filePath)
	if err != nil {
		log.Fatalf("Failed to open CSV file: %v", err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.FieldsPerRecord = -1
	records, err := reader.ReadAll()
	if err != nil {
		log.Fatalf("Failed to read CSV: %v", err)
	}

	if len(records) == 0 {
		log.Fatalf("CSV file is empty")
	}

	headers := records[0]
	restaurantMap = make(map[string]Restaurant)

	for _, row := range records[1:] {
		data := make(map[string]string)
		for i, value := range row {
			if i < len(headers) {
				data[headers[i]] = value
			}
		}
		restaurant := Restaurant{
			RestaurantID:    data["Restaurant ID"],
			RestaurantName:  data["Restaurant Name"],
			Locality:        data["Locality"],
			Cuisines:        data["Cuisines"],
			AggregateRating: data["Aggregate rating"],
			CountryCode:     data["Country Code"],
		}
		restaurantMap[restaurant.RestaurantID] = restaurant
		restaurantList = append(restaurantList, restaurant)
	}
}

func main() {
	loadCSVData("archive/zomato.csv")

	r := gin.Default()
	r.Use(cors.Default())

	// Fixed route path
	r.GET("/api/restaurant/:id", func(c *gin.Context) {
		id := c.Param("id")
		if restaurant, ok := restaurantMap[id]; ok {
			c.JSON(http.StatusOK, restaurant)
		} else {
			c.JSON(http.StatusNotFound, gin.H{"error": "Restaurant not found"})
		}
	})

	r.GET("/api/restaurants", func(c *gin.Context) {
		pageStr := c.DefaultQuery("page_number", "1")
		perPageStr := c.DefaultQuery("per_page", "10")
		search := strings.ToLower(c.DefaultQuery("search_query", ""))
		cuisine := strings.ToLower(c.DefaultQuery("cuisine", ""))
		country := c.DefaultQuery("country", "")
 
		page, err := strconv.Atoi(pageStr)
		if err != nil || page < 1 {
			page = 1
		}
		perPage, err := strconv.Atoi(perPageStr)
		if err != nil || perPage < 1 {
			perPage = 10
		}

		start := (page - 1) * perPage
		end := start + perPage

		var filtered []Restaurant
		for _, r := range restaurantList {
			if (search == "" || strings.Contains(strings.ToLower(r.RestaurantName), search)) &&
				(cuisine == "" || strings.Contains(strings.ToLower(r.Cuisines), cuisine)) &&
				(country == "" || r.CountryCode == country) {
				filtered = append(filtered, r)
			}
		}

		if start > len(filtered) {
			start = len(filtered)
		}
		if end > len(filtered) {
			end = len(filtered)
		}

		c.JSON(http.StatusOK, gin.H{
			"page":        page,
			"per_page":    perPage,
			"total":       len(filtered),
			"restaurants": filtered[start:end],
		})
	})

	r.GET("/api/filter", func(c *gin.Context) {
		// ===== Unique Cuisines =====
		cuisineSet := make(map[string]bool)
		for _, r := range restaurantList {
			cuisines := strings.Split(r.Cuisines, ",")
			for _, cuisine := range cuisines {
				trimmed := strings.TrimSpace(cuisine)
				if trimmed != "" {
					cuisineSet[trimmed] = true
				}
			}
		}
		var uniqueCuisines []string
		for cuisine := range cuisineSet {
			uniqueCuisines = append(uniqueCuisines, cuisine)
		}
	
		// ===== Country Codes from Excel =====
		f, err := excelize.OpenFile("archive/Country-code.xlsx")
		if err != nil {
			log.Printf("Failed to open Excel file: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read country code file"})
			return
		}
	
		rows, err := f.GetRows("Sheet1")  
		if err != nil {
			log.Printf("Failed to read rows from Excel: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to parse Excel"})
			return
		}
	
		var countryCodes []CountryCode
		for i, row := range rows {
			if i == 0 || len(row) < 2 {
				continue 
			}
			countryCodes = append(countryCodes, CountryCode{
				ID:   row[0],
				Name: row[1],
			})
		}
	
		 
		c.JSON(http.StatusOK, gin.H{
			"cuisines":      uniqueCuisines,
			"country_codes": countryCodes,
		})
	})
	r.NoRoute(func(c *gin.Context) {
		path := "./build" + c.Request.URL.Path
		if _, err := os.Stat(path); os.IsNotExist(err) {
			 
			c.File("./build/index.html")
		} else {
			c.File(path)
		}
	})
	log.Println("Server started at http://localhost:8080")
	r.Run(":8080")
}