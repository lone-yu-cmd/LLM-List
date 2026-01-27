package llmlist

import (
	_ "embed"
	"encoding/json"
	"fmt"
)

//go:embed data/llm_registry.json
var RegistryJSON []byte

// Registry represents the root structure of the registry
type Registry struct {
	Version   string     `json:"version"`
	UpdatedAt string     `json:"updated_at"`
	Providers []Provider `json:"providers"`
}

// Provider represents an LLM provider
type Provider struct {
	ID          string                 `json:"id"`
	Name        string                 `json:"name"`
	Description string                 `json:"description"`
	Website     string                 `json:"website"`
	Models      []Model                `json:"models"`
	APIConfig   map[string]interface{} `json:"api_config"`
}

// Model represents a specific LLM model
type Model struct {
	ID          string   `json:"id"`
	Name        string   `json:"name"`
	Type        string   `json:"type"`
	Description string   `json:"description"`
	Features    []string `json:"features"`
}

var globalRegistry *Registry

// LoadRegistry parses the embedded JSON data into a Registry struct
func LoadRegistry() (*Registry, error) {
	if globalRegistry != nil {
		return globalRegistry, nil
	}

	var registry Registry
	err := json.Unmarshal(RegistryJSON, &registry)
	if err != nil {
		return nil, fmt.Errorf("failed to parse registry JSON: %w", err)
	}
	globalRegistry = &registry
	return &registry, nil
}

// GetProviders returns all providers
func GetProviders() ([]Provider, error) {
	reg, err := LoadRegistry()
	if err != nil {
		return nil, err
	}
	return reg.Providers, nil
}

// GetProvider returns a provider by ID
func GetProvider(providerID string) (*Provider, error) {
	providers, err := GetProviders()
	if err != nil {
		return nil, err
	}
	for _, p := range providers {
		if p.ID == providerID {
			return &p, nil
		}
	}
	return nil, nil
}

// GetModels returns all models for a specific provider
func GetModels(providerID string) ([]Model, error) {
	provider, err := GetProvider(providerID)
	if err != nil {
		return nil, err
	}
	if provider == nil {
		return []Model{}, nil
	}
	return provider.Models, nil
}

// GetAllChatModels returns all chat models across all providers
// It returns a slice of models enriched with provider ID
type ChatModel struct {
	Model
	ProviderID   string `json:"provider_id"`
	ProviderName string `json:"provider_name"`
}

func GetAllChatModels() ([]ChatModel, error) {
	providers, err := GetProviders()
	if err != nil {
		return nil, err
	}

	var allModels []ChatModel
	for _, p := range providers {
		for _, m := range p.Models {
			if m.Type == "chat" {
				allModels = append(allModels, ChatModel{
					Model:        m,
					ProviderID:   p.ID,
					ProviderName: p.Name,
				})
			}
		}
	}
	return allModels, nil
}
