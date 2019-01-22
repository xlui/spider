package main

import (
	"gospider/config"
	"gospider/context"
	"log"
	"net/http"
	"os"
	"time"
)

func initialize() (ctx *context.Context, client *http.Client) {
	err := os.MkdirAll(config.Storage, 0777)
	if err != nil {
		log.Fatalln("Failed to create image folder!", err.Error())
	}

	return &context.Context{
		PageState:    map[string]int{},
		ImageState:   map[string]int{},
		PageChannel:  make(chan *context.Page, config.ChannelSize),
		ParseChannel: make(chan *context.Page, config.ChannelSize),
		ImageChannel: make(chan *context.Image, config.ChannelSize),
	}, &http.Client{}
}

func monitor(ctx *context.Context) {
	ticker := time.NewTicker(config.Interval)
	logger := "\n========================================================\n"
	logger += "queue:page(%v)\timage(%v)\tparse(%v)\nimage:found(%v)\n"
	logger += "========================================================\n"
	for {
		select {
		case <-ticker.C:
			log.Printf(logger, len(ctx.PageChannel), len(ctx.ImageChannel), len(ctx.ParseChannel), len(ctx.ImageState))
			if len(ctx.PageChannel) == 0 && len(ctx.ParseChannel) == 0 && len(ctx.ImageChannel) == 0 {
				log.Println("All images downloaded!")
				os.Exit(0)
			}
		}
	}
}

func main() {
	ctx, client := initialize()

	for i := 0; i < config.Fetchers; i++ {
		go func() {
			for pg := range ctx.PageChannel {
				pg.Fetch(ctx, client)
			}
		}()
	}

	for i := 0; i < config.Fetchers; i++ {
		go func() {
			for parse := range ctx.ParseChannel {
				parse.Parse(ctx)
			}
		}()
	}

	for i := 0; i < config.Downloaders; i++ {
		go func() {
			for img := range ctx.ImageChannel {
				img.Download(ctx, client)
			}
		}()
	}

	ctx.PageChannel <- &context.Page{Url: config.Root, Number: 1, Parsed: true}
	monitor(ctx)
}
