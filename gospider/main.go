package main

import (
	"fmt"
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
		ImageCount:   make(chan int),
	}, &http.Client{}
}

func monitor(ctx *context.Context) {
	done := true
	count := 0
	ticker := time.NewTicker(config.Interval)
	logger := "\n========================================================\n"
	logger += "queue:page(%v)\timage(%v)\tparse(%v)\nimage:found(%v)\tdone(%v)\n"
	logger += "========================================================\n"
	for {
		select {
		case <-ticker.C:
			log.Printf(logger, len(ctx.PageChannel), len(ctx.ImageChannel), len(ctx.ParseChannel), len(ctx.ImageState), count)
			if len(ctx.PageChannel) == 0 && len(ctx.ParseChannel) == 0 && len(ctx.ImageChannel) == 0 {
				for _, val := range ctx.ImageState {
					if val != config.Success {
						done = false
						break
					}
				}
				if done {
					log.Println("All images downloaded!")
					os.Exit(0)
				}
			}
		case c := <-ctx.ImageCount:
			count += c
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

	for i := 1; i <= config.PageCount; i++ {
		// http://www.zeroorez.net/beauty?pn=1
		url := fmt.Sprint(config.Root, "?pn=", i)
		ctx.PageChannel <- &context.Page{
			Url:    url,
			Number: i,
			Parsed: true,
		}
	}
	monitor(ctx)
}
